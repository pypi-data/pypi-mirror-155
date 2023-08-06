
# File: util.py 
# Author(s): Saswati Ray
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import logging, uuid

__version__ = "0.1.0"

from d3m.container.dataset import D3MDatasetLoader, Dataset
from d3m.metadata import base as metadata_base, problem
from d3m.metadata.base import Metadata
from d3m.metadata.pipeline import Pipeline, PrimitiveStep
import os, json
import pickle
import pandas as pd
import numpy as np

# AutonML imports
import autonml.solutiondescription as solutiondescription
import autonml.problem_pb2 as problem_pb2

def load_problem_doc(problem_doc_uri: str):
    """     
    Load problem_doc from problem_doc_uri     
    Parameters     ---------     
    problem_doc_uri     Uri where the problemDoc.json is located
    """
    with open(problem_doc_uri) as file:
        problem_doc = json.load(file)
    problem_doc_metadata = Metadata(problem_doc)
    return problem_doc_metadata

def add_target_columns_metadata(dataset: 'Dataset', problem_doc: 'Metadata'):

    for data in problem_doc['inputs']:
        targets = data['targets']
        for target in targets:
            semantic_types = list(dataset.metadata.query((target['resource_id'], metadata_base.ALL_ELEMENTS, target['column_index'])).get('semantic_types', []))
            if 'https://metadata.datadrivendiscovery.org/types/Target' not in semantic_types:
                semantic_types.append('https://metadata.datadrivendiscovery.org/types/Target')
                dataset.metadata = dataset.metadata.update((target['resource_id'], metadata_base.ALL_ELEMENTS, target['column_index']), {'semantic_types': semantic_types})
            if 'https://metadata.datadrivendiscovery.org/types/TrueTarget' not in semantic_types:
                semantic_types.append('https://metadata.datadrivendiscovery.org/types/TrueTarget')
                dataset.metadata = dataset.metadata.update((target['resource_id'], metadata_base.ALL_ELEMENTS, target['column_index']), {'semantic_types': semantic_types})
            dataset.metadata = dataset.metadata.remove_semantic_type((target['resource_id'], 
            metadata_base.ALL_ELEMENTS, target['column_index']),'https://metadata.datadrivendiscovery.org/types/Attribute',)

    return dataset

def add_privileged_columns_metadata(dataset: 'Dataset', problem_doc: 'Metadata'):
    for privileged_data in problem_doc.get('inputs')[0].get('privileged_data', []):
        dataset.metadata = dataset.metadata.add_semantic_type((privileged_data['resource_id'], metadata_base.ALL_ELEMENTS, privileged_data['column_index']),'https://metadata.datadrivendiscovery.org/types/PrivilegedData',)

    return dataset

def add_target_metadata(dataset, targets):
    for target in targets:
        semantic_types = list(dataset.metadata.query((target.resource_id, metadata_base.ALL_ELEMENTS, target.column_index)).get('semantic_types', []))
        if 'https://metadata.datadrivendiscovery.org/types/Target' not in semantic_types:
            semantic_types.append('https://metadata.datadrivendiscovery.org/types/Target')
            dataset.metadata = dataset.metadata.update((target.resource_id, metadata_base.ALL_ELEMENTS, target.column_index), {'semantic_types': semantic_types})
        if 'https://metadata.datadrivendiscovery.org/types/TrueTarget' not in semantic_types:
            semantic_types.append('https://metadata.datadrivendiscovery.org/types/TrueTarget')
            dataset.metadata = dataset.metadata.update((target.resource_id, metadata_base.ALL_ELEMENTS, target.column_index), {'semantic_types': semantic_types})
        dataset.metadata = dataset.metadata.remove_semantic_type((target.resource_id,
        metadata_base.ALL_ELEMENTS, target.column_index),'https://metadata.datadrivendiscovery.org/types/Attribute',)

    return dataset

def add_privileged_metadata(dataset: 'Dataset', privileged_data):
    for data in privileged_data:
        dataset.metadata = dataset.metadata.add_semantic_type((data.resource_id, metadata_base.ALL_ELEMENTS, data.column_index),'https://metadata.datadrivendiscovery.org/types/PrivilegedData',)

    return dataset

def get_task(names):
    tasks = ['SEMISUPERVISED', 'OBJECTDETECTION', 'FORECASTING', 'GRAPHMATCHING', 'VERTEXNOMINATION', 'VERTEXCLASSIFICATION', \
             'COMMUNITYDETECTION', 'LINKPREDICTION', 'COLLABORATIVEFILTERING', 'CLUSTERING', 'REMOTESENSING', \
             'CLASSIFICATION', 'REGRESSION']
    for t in tasks:
        if t in names:
            if t == 'LINKPREDICTION':
                if 'TIMESERIES' in names:
                    return 'LINKPREDICTIONTIMESERIES'
            return t
    return None
        
def get_task_name(keywords):
    names = get_task_list(keywords)
    return get_task(names)

def get_task_list(keywords):
    names = []
    for k in keywords:
        name = k.upper()
        names.append(name)
    return names
 
def load_data_problem(inputdir, problempath):
    print("Reading ", inputdir)
    print("Reading ", problempath)

    with open(problempath) as file:
        problem_schema =  json.load(file)

    datasetId = problempath[:-29]
    dataset_schema = datasetId + "dataset_TRAIN/datasetDoc.json"
    problem_doc_metadata = Metadata(problem_schema)
    dataset_uri = 'file://{dataset_uri}'.format(dataset_uri=dataset_schema)
    dataset = D3MDatasetLoader().load(dataset_uri)

    problem_description = problem.parse_problem_description(problempath)
    dataset = add_target_columns_metadata(dataset, problem_description)
    dataset = add_privileged_columns_metadata(dataset, problem_description)
    taskname = get_task_name(problem_doc_metadata.query(())['about']['taskKeywords'])
    metric = problem_doc_metadata.query(())['inputs']['performanceMetrics'][0]['metric']
    posLabel = None
    if metric == "f1":
        posLabel = problem_doc_metadata.query(())['inputs']['performanceMetrics'][0]['posLabel']

    # Read the data augmentation
    keywords = getAugmentation_keywords(problem_doc_metadata)
  
    return (dataset, taskname, problem_description, metric, posLabel, keywords)

def load_testdata(problempath):
    datasetId = problempath[:-35]
    print("Id = ", datasetId)
    dataset_schema = datasetId + "/TEST/dataset_TEST/datasetDoc.json"
    dataset_uri = 'file://{dataset_uri}'.format(dataset_uri=dataset_schema)
    dataset = D3MDatasetLoader().load(dataset_uri)
    return dataset

def getAugmentation_keywords(problem_doc_metadata):
    keywords = None
    if "dataAugmentation" in problem_doc_metadata.query(()):
        keywords = problem_doc_metadata.query(())["dataAugmentation"]
    return keywords

def get_pipeline(dirname, pipeline_name):
    newdirname = dirname + "/" + pipeline_name
    filename = pipeline_name.split("_")[0]
    f = newdirname + "/" + filename + ".dump"

    solution = pickle.load(open(f, 'rb'))
    return solution

def write_solution(solution, dirname):
    rank = str(solution.rank)
    supporting_dirname = dirname + "/" + solution.id + "_" + rank
    if not os.path.exists(supporting_dirname):
        os.makedirs(supporting_dirname)
    output = open(supporting_dirname+"/"+solution.id+".dump", "wb")
    pickle.dump(solution, output)
    output.close()

def initialize_for_search(outputDir):
    name = outputDir
    if not os.path.exists(name):
        os.makedirs(name)

    dirNames = [outputDir+"/executables", outputDir+"/predictions", outputDir+"/pipelines_searched", outputDir+"/pipelines_scored", \
                outputDir+"/pipelines_ranked", outputDir+"/pipeline_runs", outputDir+"/subpipelines", outputDir+"/additional_inputs",
                outputDir+"/training_predictions"]
   
    for name in dirNames: 
        if not os.path.exists(name):
           os.makedirs(name)

def write_predictions(predictions, dirname, request_id):
    directory = dirname + "/" + str(request_id)
    if not os.path.exists(directory):
        os.makedirs(directory)

    outputFilePath = directory + "/predictions.csv"
    with open(outputFilePath, 'w') as outputFile:
        predictions.to_csv(outputFile, header=True, index=False)
    return outputFilePath
  
def write_feature_importances(feature_importances, dirname, request_id):
    directory = dirname + "/" + str(request_id)
    if not os.path.exists(directory):
        os.makedirs(directory)

    outputFilePath = directory + "/feature_importances.csv"
    with open(outputFilePath, 'w') as outputFile:
        feature_importances.to_csv(outputFile, header=True, index=False)
    return outputFilePath
 
def write_pipeline_json(solution, primitives, solution_dict, dirName, subpipeline_dirName, rank=None, train_score=None):
    solution.write_pipeline_json(primitives, solution_dict, dirName, subpipeline_dirName, rank, train_score) 

def write_rank_file(solution, rank, dirName):
    outputFilePath = dirName + "/" + solution.id + ".rank"
    with open(outputFilePath, 'w') as outputFile:
        outputFile.write(str(rank))
    
def write_pipeline_yaml(solution, dirname, dataset, problem_description):
    run_id = str(uuid.uuid4())
    filename = dirname + "/" + run_id + ".yaml"
    solution.write_pipeline_run(problem_description, dataset, filename)

def write_pipeline_executable(solution, dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    shell_script = '#!/bin/bash\n python ./autonml/main.py test\n'
    filename = dirname + "/" + solution.id + "_" + str(solution.rank) + ".sh"
    with open(filename, 'w') as f:
        f.write(shell_script)
    os.chmod(filename, 0o755)

def invert_metric(metric_type):
    min_metrics = set()
    min_metrics.add("MEAN_SQUARED_ERROR")
    min_metrics.add("ROOT_MEAN_SQUARED_ERROR")
    min_metrics.add("MEAN_ABSOLUTE_ERROR")
    min_metrics.add("LOSS")
    min_metrics.add("HAMMING_LOSS")
    if metric_type in min_metrics:
        return True
    return False

def get_distil_metric_name(metric_type):
    metric = 'accuracy'
    if metric_type == "MEAN_SQUARED_ERROR" or metric_type == "ROOT_MEAN_SQUARED_ERROR" or metric_type == "MEAN_ABSOLUTE_ERROR":
        metric = 'meanSquaredError'
    elif metric_type == "MEAN_ABSOLUTE_ERROR":
        metric = 'meanAbsoluteError'
    elif metric_type == "ACCURACY":
        metric = 'accuracy'
    elif metric_type == "F1_MACRO" or metric_type == "F1_MICRO" or metric_type == "F1":
        metric_type == 'f1Macro'
    return metric

