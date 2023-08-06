# File: main.py 
# Author(s): Saswati Ray, Vedant Sanil
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

from ctypes import ArgumentError
import logging
from multiprocessing import set_start_method
set_start_method("spawn", force=True)
from concurrent import futures
import time
import sys
import os
import json
from pathlib import Path
import shutil
import warnings
import subprocess

warnings.filterwarnings("ignore")
sys.path.append(f'{os.getcwd()}/autonml/')

import grpc
from multiprocessing import cpu_count

# AutonML imports
import autonml.search as search
from autonml.api_v3 import core

TA2_API_HOST = '[::]'
TA2_API_PORT = 45042

def garbage_collect():

    # TODO (vedant) : garbage collection for NBeats is being done
    # for kungfuai primitives. This needs to be resolved within
    # kungfuai NBeats
    if os.path.exists(os.path.join(os.getcwd(), "nbeats_weights")):
        shutil.rmtree(os.path.join(os.getcwd(), "nbeats_weights"))


def get_run_id(output_dir):
        # Get the most recent run
        run_dirs = [os.path.join(output_dir, f) for f in os.listdir(output_dir)]
        output_dir = sorted(run_dirs, key=lambda x: os.path.getmtime(x), reverse=True)[0]

        return output_dir

def prerun_error_check():
    if len(sys.argv) < 7 or len(sys.argv) > 8:
        arg_err_str = "Incorrect number of arguments provided. Required arguments (in order): \n\t-Run type (fit/fit-produce/produce) \n\t-Input Directory \n\t-Output Directory \n\t-Timeout(in minutes) \n\t-Number of CPU cores \n\t-D3M Problem Path (please refer to AutonML's documentation for more details \n\n Optional arguments \n\t-D3M Static directory: stores weight files\n"
        raise ArgumentError(arg_err_str)

    if sys.argv[1] != 'fit' and sys.argv[1] != 'fit-produce' and sys.argv[1] != 'produce':
        raise ArgumentError(f"Run type argument is invalid. It must either be fit, fit-produce, or produce. Argument provided by user for run-type: {sys.argv[1]}")

    if not os.path.exists(sys.argv[2]):
        raise FileNotFoundError(f"Input directory provided ({sys.argv[2]}) does not exist")

    if not os.path.exists(sys.argv[6]):
        raise FileNotFoundError(f"Problem Path file provided ({sys.argv[6]}) does not exist")

    if len(sys.argv) == 8:
        if not os.path.exists(sys.argv[7]):
            raise FileNotFoundError(f"Static directory provided ({sys.argv[7]}) does not exist")

def main_run():
    '''Main API to invoke complete AutonML pipeline'''

    if not os.path.exists(sys.argv[3]):
        logging.warning(f"Output directory does not exist, creating Output directory at path: {sys.argv[3]}")

        output_path = Path(sys.argv[3])

        if not output_path.parent.exists():
            # TODO (vedant) : should parent directories be created recursively too?
            raise FileNotFoundError(f"Parent directory {output_path.parent()} for provided output path: {sys.argv[3]} does not exist. Please recheck that the provided parent path is correct")
        else:
            os.mkdir(sys.argv[3])

    # Perform a preliminary error check to ensure number of arguments and directories supplied are correct
    prerun_error_check()

    # Remove all files in output directory
    output_dir = sys.argv[3]
    for search_dir in os.listdir(output_dir):
        search_dir_path = os.path.join(output_dir, search_dir)
        shutil.rmtree(search_dir_path)

    # Search is invoked first to create optimal pipelines
    main_search()

    # Fit and evaluate across searched pipelines
    # TODO (vedant) : error checks here
    run_pipeline(output_dir, sys.argv[1])

    # Save environment variables in a file
    search_dir_path = get_run_id(sys.argv[3])
    filepath = os.path.join(search_dir_path, 'environment_variables.json')
    
    env_dict = {}
    env_dict['D3MINPUTDIR'] = os.environ['D3MINPUTDIR']
    env_dict['D3MSTATICDIR'] = os.environ['D3MSTATICDIR']
    env_dict['D3MOUTPUTDIR'] = os.environ['D3MOUTPUTDIR']
    env_dict['D3MTIMEOUT'] = os.environ['D3MTIMEOUT']
    env_dict['D3MCPU'] = (int)(os.environ['D3MCPU'])

    with open(filepath, "w") as fp:
        json.dump(env_dict, fp)

    # Garbage collect any leftover intermediate variables
    garbage_collect()


def run_pipeline(output_dir, run_method):

    # TODO (vedant) : Error checking on valid directory paths?
    # Code to score the output, and write to the $D3MOUTPUTDIR directory
    for search_dir in os.listdir(output_dir):
        search_dir_path = os.path.join(output_dir, search_dir)
        pipeline_dir_path = os.path.join(search_dir_path, 'pipelines_ranked')

        for idx, jsonfile in enumerate(os.listdir(pipeline_dir_path)):
            jsonfile_path = os.path.join(pipeline_dir_path, jsonfile)
            prediction_name = jsonfile.replace('.json', '')
            logging.critical(f'Evaluating over JSON File {idx+1}/{len(os.listdir(pipeline_dir_path))}: {jsonfile_path}\n')
            
            if run_method == 'fit-produce':
                p = subprocess.Popen([sys.executable, '-m', 'd3m', 'runtime', '-v',
                                    os.environ['D3MSTATICDIR'], 'fit-produce', '-p',
                                    jsonfile_path, '-r', os.path.join(os.environ['D3MINPUTDIR'], 'TRAIN/problem_TRAIN/problemDoc.json'),
                                    '-i', os.path.join(os.environ['D3MINPUTDIR'], 'TRAIN/dataset_TRAIN/datasetDoc.json'), '-t',
                                    os.path.join(os.environ['D3MINPUTDIR'], 'TEST/dataset_TEST/datasetDoc.json'), '-o',
                                    os.path.join(search_dir_path, 'predictions', f'{prediction_name}.predictions.csv')], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            elif run_method == 'fit':
                p = subprocess.Popen([sys.executable, '-m', 'd3m', 'runtime', '-v',
                                    os.environ['D3MSTATICDIR'], 'fit', '-p',
                                    jsonfile_path, '-r', os.path.join(os.environ['D3MINPUTDIR'], 'TRAIN/problem_TRAIN/problemDoc.json'),
                                    '-i', os.path.join(os.environ['D3MINPUTDIR'], 'TRAIN/dataset_TRAIN/datasetDoc.json')], 
                                    stderr=subprocess.PIPE)

            _, error = p.communicate()
            if p.returncode != 0:
                raise RuntimeError(error.decode())

            # Generate code that converts JSON to python code
            src_dir = os.path.dirname(os.path.abspath(__file__))

            subprocess.run([sys.executable, os.path.join(src_dir, 'mkpline.py'), 
                                jsonfile_path, os.path.join(search_dir_path, 'executables', f'{prediction_name}.code.py')],
                                stdout=sys.stdout, stderr=sys.stdout, check=True)


def main_search():
    '''API called only during search'''
    # TODO (vedant) : error handling if number of args provided is less than zero? 
    # is this very necessary ?

    # TODO (vedant) : pass D3m specific variables directly instead of environment 
    # variables
    logging.info('RUNNING SEARCH')

    os.environ['D3MINPUTDIR'] = sys.argv[2]
    os.environ['D3MOUTPUTDIR'] = sys.argv[3]
    os.environ['D3MTIMEOUT'] = sys.argv[4]
    os.environ['D3MCPU'] = sys.argv[5]
    os.environ['D3MPROBLEMPATH'] = sys.argv[6]

    if len(sys.argv) == 8:
        os.environ['D3MSTATICDIR'] = sys.argv[7]
    else:
        os.environ['D3MSTATICDIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

    search.search_phase()

def main(argv):
    mode = argv[0]
    logging.info("Running in mode %s", mode)

    if mode == "search":
        search.search_phase()
    else:
        threadpool = futures.ThreadPoolExecutor(max_workers=cpu_count())
        server = grpc.server(threadpool)
        core.add_to_server(server)
        server_string = '{}:{}'.format(TA2_API_HOST, TA2_API_PORT)
        server.add_insecure_port(server_string)
        logging.critical("Starting server on %s", server_string)
        server.start()
        logging.critical("Server started, waiting.")
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            server.stop(0)

if __name__ == '__main__':
    #main(sys.argv[1:])
    main_run()
