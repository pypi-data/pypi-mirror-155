
# File: search.py 
# Author(s): Saswati Ray
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import os, sys, uuid
import logging
from multiprocessing import Pool, cpu_count
from timeit import default_timer as timer

# AutonML imports
import autonml.util as util
import autonml.auto_solutions as auto_solutions
import autonml.problem_pb2 as problem_pb2
import autonml.primitive_lib as primitive_lib

def rank_solutions(valid_solution_scores, problem_metric):
    """
    Return sorted list of multiple solutions.
    """
    # Sort solutions by their scores and rank them
    import operator
    sorted_x = sorted(valid_solution_scores.items(), key=operator.itemgetter(1))
    if util.invert_metric(problem_metric) is False:
        sorted_x.reverse()
    return sorted_x

def search_phase():
    """
    TA2 running in stand-alone search phase
    """
    
    overall_start = timer()
    inputDir = os.environ['D3MINPUTDIR']
    outputDir = os.environ['D3MOUTPUTDIR']
    timeout_env = os.environ['D3MTIMEOUT']
    num_cpus = (int)(os.environ['D3MCPU'])
    problemPath = os.environ['D3MPROBLEMPATH']

    logger = logging.getLogger()
    logger.setLevel(level=logging.ERROR)
    print("D3MINPUTDIR = ", inputDir)
    print("D3MOUTPUTDIR = ", outputDir)
    print("timeout = ", timeout_env)
    print("cpus = ", num_cpus)
    (dataset, task_name, problem_desc, metric, posLabel, keywords) = util.load_data_problem(inputDir, problemPath)
    testds = None #util.load_testdata(problemPath)

    async_message_thread = Pool(int(num_cpus))
    valid_solutions = {}
    valid_solution_scores = {}

    print("Metric = ", metric, " poslabel = ", posLabel)
    timeout_in_min = (int)(timeout_env)
    primitives = primitive_lib.load_primitives()
    print(task_name)

    problem_metric = "F1_MACRO"
    if metric == 'f1Macro':
        problem_metric = "F1_MACRO"
    elif metric == 'f1': 
        problem_metric = "F1"
    elif metric == 'accuracy':
        problem_metric = "ACCURACY"
    elif metric == 'meanSquaredError':
        problem_metric = "MEAN_SQUARED_ERROR"
    elif metric == 'rootMeanSquaredError':
        problem_metric = "ROOT_MEAN_SQUARED_ERROR"
    elif metric == 'meanAbsoluteError':
        problem_metric = "MEAN_ABSOLUTE_ERROR"
    elif 'rocAuc' in metric:
        problem_metric = "ROC_AUC"
    elif 'rSquared' in metric:
        problem_metric = "R_SQUARED"

    # Still run the normal pipeline even if augmentation
    start = timer()

    automl = auto_solutions.auto_solutions(task_name, None)
    solutions = automl.get_solutions(dataset, problem_metric, timeout_in_min)
    end = timer()
    time_used = end - start
    logging.critical("Time used up: %f seconds", time_used)

    inputs = []
    inputs.append(dataset)

    search_id_str = str(uuid.uuid4())
    outputDir = os.environ['D3MOUTPUTDIR'] + "/" + search_id_str
    util.initialize_for_search(outputDir)

    # Score potential solutions
    training_preds_dir = outputDir + "/training_predictions" 
    results = [async_message_thread.apply_async(evaluate_solution_score, (inputs, sol, primitives, problem_metric, posLabel, None, training_preds_dir,)) for sol in solutions]

    timeout = timeout_in_min * 60
    if timeout <= 0:
        timeout = None
    elif timeout > 60:
        timeout = timeout - 60

    if timeout is not None:
        timeout = timeout - time_used

    index = 0
    for r in results:
        try:
            start = timer()
            (score, optimal_params) = r.get(timeout=timeout)
            valid_solution_scores[index] = score
            if optimal_params is not None and len(optimal_params) > 0:
                solutions[index].set_hyperparams(None, optimal_params)
            end = timer()
            time_used = end - start
            timeout = timeout - time_used
            timeout = max(5, timeout)
        except:
            print(solutions[index].primitives)
            print(sys.exc_info()[0])
            print("Solution terminated: ", solutions[index].id)
        index = index + 1

    # Sort solutions by their scores and rank them
    sorted_x = rank_solutions(valid_solution_scores, problem_metric)

    rank = 1
    for (index, score) in sorted_x:
        id = solutions[index].id
        valid_solutions[id] = solutions[index]
        valid_solutions[id].rank = rank
        print("Rank ", rank)
        print("Score ", score)
        print(valid_solutions[id].primitives)
        rank = rank + 1

    num = 20
    if len(sorted_x) < 20:
        num = len(sorted_x)

    # Fit solutions and dump out files
    sorted_x = sorted_x[:num]
    testdata=[]
    testdata.append(testds)
    results = [async_message_thread.apply_async(fit_solution, (inputs, testdata, solutions[index], primitives, outputDir, problem_desc, score))
     for (index,score) in sorted_x]

    index = 0
    for r in results:
        try:
            valid=r.get(timeout=None)
        except:
            print(solutions[sorted_x[index][0]].primitives)
            print(sys.exc_info()[0])
            print("Fit Solution terminated: ", solutions[sorted_x[index][0]].id)
        index = index + 1

    overall_end = timer()
    logging.critical("Time used by AutonML : %f seconds", (overall_end - overall_start))

def evaluate_solution_score(inputs, solution, primitives, metric, posLabel, sol_dict, training_preds_dir=None):
    """
    Scores each potential solution
    Runs in a separate process
    """
    print("Evaluating pipeline: ", solution.id)

    (score, optimal_params) = solution.score_solution(inputs=inputs, metric=metric, posLabel=posLabel,
                                primitive_dict=primitives, solution_dict=sol_dict, mode=training_preds_dir)

    return (score, optimal_params)

def fit_solution(inputs, testdata, solution, primitives, outputDir, problem_desc, score):
    """
    Fits each potential solution
    Runs in a separate process
    """
    print("Fitting pipeline: ", solution.id)

    #output = solution.fit(inputs=inputs, solution_dict=None)
    #output = solution.produce(inputs=testdata, solution_dict=None)
    util.write_pipeline_json(solution, primitives, None, outputDir + "/pipelines_ranked", outputDir + "/subpipelines", rank=solution.rank, train_score=score)
    #util.write_pipeline_yaml(solution, outputDir + "/pipeline_runs", inputs, problem_desc)
    (stepname, feature_imp) = solution.produce_feature_importances(None)
    if feature_imp is not None:
        uri = util.write_feature_importances(feature_imp, outputDir + "/predictions", "12345")
        print(uri)
    return True
