
# File: auto_solutions.py 
# Author(s): Saswati Ray
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import os, copy, uuid, sys
import logging
import numpy as np
import traceback

# AutonML imports
import autonml.util as util
import autonml.solutiondescription as solutiondescription
import autonml.solution_templates as solution_templates
import autonml.default_hyperparams as default_hyperparams
import autonml.helper_functions as helper_functions

def is_primitive_reasonable(python_path, rows, total_cols, types_present, task_name, metric):
    """
    Rule-based elimination based on ML task, dataset size (rows, cols).
    Is primitive reasonable to evaluate for the ML task, dataset size?
    Eliminate expensive solutions here!!!
    """
    if 'ROC_AUC' in metric and \
       ('passive' in python_path or \
        'discriminant' in python_path or \
        'svc' in python_path):
        return False

    if (total_cols > 1000 or rows > 100000) and 'xgboost' in python_path:
        return False

    if total_cols > 2000 and ('discriminant' in python_path or 'passive' in python_path):
        return False

    if (total_cols > 100 or rows > 100000) and 'k_neighbors' in python_path:
        return False

    if complex_types_present(types_present) is True and \
       ('ada_boost' in python_path or \
        'passive_aggressive' in python_path or \
        'xgboost' in python_path or \
        'gradient_boosting' in python_path or \
        'quadratic' in python_path or \
        'mlp' in python_path or \
        'bagging' in python_path):
        return False

    # Forecasting
    if task_name == "FORE_REGRESSION" and 'mlp' in python_path:
        return False

    # SVM gets extremely expensive (memory) for >10k samples!!!
    if rows > 10000 and 'classification.svc.SKlearn' in python_path:
        return False

    if rows >= 100000 and ('gradient_boosting' in python_path or 'mlp.SKlearn' in python_path or 'ada_boost' in python_path or 'passive_aggressive' in python_path):
        return False

    if rows > 1000000 and ('bagging' in python_path or 'elastic' in python_path or 'lasso_cv' in python_path):
        return False

    return True

def complex_types_present(types_present):
    """
    Does datatypes contain multi-media??
    """
    if types_present is None:
        return False
    if 'AUDIO' in types_present or \
       'VIDEO' in types_present or \
       'IMAGE' in types_present:
        return True
    return False

class auto_solutions(object):
    """
    Main class representing the AutoML (pipeline constructor) for TA2.
    A "pipeline" and "solution" will mean the SAME thing in D3M.
    Creates a suite of suitable pipelines for a given dataset/problem type.
    Pipelines/Solutions are only created using templates and not run here.
    In case of tasks with multiple pipelines (classification/regression/SSL), primary data processing/featurization steps are
    run only once and cached for all the pipelines.
    """
    def __init__(self, task_name, problem = None):
        """
        Constructor
        """
        self.types_present = [] # Data types present in the dataset
        self.task_name = task_name # ML task
        self.solutions = [] # Placeholder to contain list of all pipelines for the specific dataset/problem
        self.basic_sol = None # Primary solution containing all data processing/featurization steps
        self.addn_sol = None # Secondary solution (in case of TEXT/IMAGE etc)
        self.problem = problem
        self.rows = 0
        self.total_cols = 0
        self.metric = None
        self.timeout_in_min = 0

    def add_classification_pipelines(self):
        # Add a classification pipeline too
        primitives = ['d3m.primitives.classification.random_forest.SKlearn',
                      'd3m.primitives.classification.extra_trees.SKlearn',
                      'd3m.primitives.classification.gradient_boosting.SKlearn',
                      'd3m.primitives.classification.bernoulli_naive_bayes.SKlearn']
        for p in primitives:
            pipe = self.get_solution_by_task_name('CLASSIFICATION', p)
            pipe.set_classifier_hyperparam()
            self.solutions.append(pipe)

    def add_regression_pipelines(self):
        # Add a regression pipeline too
        primitives = ['d3m.primitives.regression.random_forest.SKlearn',
                      'd3m.primitives.regression.extra_trees.SKlearn',
                      'd3m.primitives.regression.gradient_boosting.SKlearn']

        for p in primitives:
            pipe = self.get_solution_by_task_name('REGRESSION', p)
            self.solutions.append(pipe)

    def get_link_prediction_timeseries_pipelines(self):
        names = ['LINKPREDICTION','LINKPREDICTION2']
        for name in names:
            pipe = self.get_solution_by_task_name(name)
            self.solutions.append(pipe)
        self.add_regression_pipelines()

    def get_vertex_classification_pipelines(self):
        names = ['VERTEXCLASSIFICATION','VERTEXCLASSIFICATION2','VERTEXCLASSIFICATION3']
        for name in names:
            pipe = self.get_solution_by_task_name(name)
            self.solutions.append(pipe)
        self.add_classification_pipelines()
        prims = ['d3m.primitives.classification.extra_trees.SKlearn', 'd3m.primitives.classification.random_forest.SKlearn']
        for prim in prims:
            pipe = self.get_solution_by_task_name('ISI_PIPELINE', ML_prim=prim, outputstep=2, dataframestep=1)
            self.solutions.append(pipe)

    def get_graph_matching_pipelines(self):
        names = ['GRAPHMATCHING','GRAPHMATCHING2','GRAPHMATCHING3']
        for name in names:
            pipe = self.get_solution_by_task_name(name)
            self.solutions.append(pipe)
        self.add_classification_pipelines()

    def get_link_prediction_pipelines(self):
        names = ['LINKPREDICTION','LINKPREDICTION2']
        for name in names:
            pipe = self.get_solution_by_task_name(name)
            self.solutions.append(pipe)
        self.add_classification_pipelines()

    def get_collaborative_filtering_pipelines(self):
        pipe = self.get_solution_by_task_name(self.task_name)
        self.solutions.append(pipe)

        # Add a regression pipeline too
        pipe = self.get_solution_by_task_name('REGRESSION', 'd3m.primitives.regression.extra_trees.SKlearn')
        self.solutions.append(pipe)

    def get_SSL_pipelines(self, rows):
        basics = [self.basic_sol, self.addn_sol]
        construct_primitive = 'd3m.primitives.data_transformation.construct_predictions.Common'
        if 'ROC_AUC' in self.metric:
            construct_primitive='d3m.primitives.data_transformation.construct_confidence.Common'

        # Iterate through variants of possible blackbox hyperparamets.
        total_cols = self.total_cols
        for variant in solution_templates.sslVariants:
            valid = is_primitive_reasonable(variant, rows, total_cols, self.types_present, self.task_name, self.metric)
            if valid is False:
                continue

            for sol in basics:
                if sol is None:
                    continue

                pipe = copy.deepcopy(sol)
                pipe.id = str(uuid.uuid4())
                pipe.add_step('d3m.primitives.semisupervised_classification.iterative_labeling.AutonBox', outputstep = pipe.index_denormalize + 3, construct_primitive=construct_primitive)
                pipe.add_ssl_variant(variant)
                self.solutions.append(pipe)

        # Add extra pipeline too
        pipe = self.get_solution_by_task_name('SEMISUPERVISED_HDB', 'd3m.primitives.semisupervised_classification.iterative_labeling.AutonBox')
        pipe.add_ssl_variant('d3m.primitives.classification.random_forest.SKlearn')
        self.solutions.append(pipe)

    def get_community_detection_pipelines(self):
        names = ['COMMUNITYDETECTION','COMMUNITYDETECTION2']
        for name in names:
            pipe = self.get_solution_by_task_name(name)
            self.solutions.append(pipe)

    def get_clustering_pipelines(self):
        pipe = self.get_solution_by_task_name(self.task_name)
        self.solutions.append(pipe)
        self.add_classification_pipelines()

    def get_forecasting_pipelines(self, dataset):
        names = ['ARIMA_FORECASTING','VAR_FORECASTING', 'NBEATS_FORECASTING', 'DISTIL_NBEATS', 'ESRNN_FORECASTING']#,'LSTM_FORECASTING']
        for name in names:
            pipe = self.get_solution_by_task_name(name)
            self.solutions.append(pipe)
        self.task_name = 'FORE_REGRESSION'
        self.get_solutions(dataset, self.metric, self.timeout_in_min)
 
    def get_object_detection_pipelines(self):
        names = ['OBJECTDETECTION','OBJECTDETECTION2']
        for name in names:
            pipe = self.get_solution_by_task_name(name)
            self.solutions.append(pipe)

    def create_basic_solutions(self, dataset):
        """
        In case of tasks with multiple pipelines (classification/regression/SSL), primary data processing/featurization steps are
        run only once and cached for all the pipelines.
        """
        if self.task_name != 'CLASSIFICATION' and \
           self.task_name != 'REGRESSION' and \
           self.task_name != 'SEMISUPERVISED' and \
           self.task_name != 'FORE_REGRESSION' and \
           self.task_name != 'REMOTESENSING':
            return

        basic_sol = None
        try:
            # Set data types, and meta data information to begin with
            basic_sol = solutiondescription.SolutionDescription(self.problem)
            basic_sol.initialize_solution(self.task_name)
            (self.types_present, self.total_cols, self.rows, categorical_atts, ordinal_atts, ok_to_denormalize, privileged, add_floats) = helper_functions.column_types_present(dataset)
            logging.critical(self.types_present)
            basic_sol.set_add_floats(add_floats)
            basic_sol.set_categorical_atts(categorical_atts)
            basic_sol.set_ordinal_atts(ordinal_atts)
            basic_sol.set_denormalize(ok_to_denormalize)
            basic_sol.set_privileged(privileged)
            basic_sol.initialize_solution(self.task_name, self.total_cols, self.metric)
        except Exception as e:
            print(e)
            logging.error(sys.exc_info()[2])
            basic_sol = None
            self.types_present = None
            self.basic_sol = None
            return

        # For file in each data point, we treat as time series for featurization
        if len(self.types_present) == 1 and self.types_present[0] == 'FILES':
            self.types_present[0] = 'TIMESERIES'

        self.basic_sol = basic_sol

        if self.task_name == 'REMOTESENSING':
            return

        # Initialize basic solutions based on data types- TIMESERIES / IMAGE / TEXT / AUDIO / VIDEO 
        if 'TIMESERIES' in self.types_present:
            self.basic_sol.initialize_solution('TIMESERIES')
        elif 'IMAGE' in self.types_present:
            if self.rows > default_hyperparams.multimedia_threshold:
                self.basic_sol.add_splitter()
                self.rows = default_hyperparams.multimedia_threshold
            self.basic_sol.initialize_solution('IMAGE', self.total_cols, self.metric)
            self.addn_sol = copy.deepcopy(basic_sol)
            self.addn_sol.initialize_solution('IMAGE2', self.total_cols, self.metric)
        elif 'COREXTEXT' in self.types_present:
            if self.task_name == "FORE_REGRESSION": # Forecasting
                self.basic_sol.initialize_solution('DISTILTEXT', self.total_cols, self.metric)
                self.basic_sol.set_distil_text_hyperparam()
            else: # Classification / Regression
                self.basic_sol.initialize_solution('DISTILTEXT', self.total_cols, self.metric)
                if self.task_name == 'REGRESSION':
                    self.basic_sol.set_distil_text_hyperparam()
                if self.rows < 1000000: # Add Corex pipelines for rows < 1000K
                    self.addn_sol = copy.deepcopy(basic_sol)
                    self.addn_sol.initialize_solution('COREXTEXT', self.total_cols, self.metric)
                if self.rows < 100000: # Add TFIDF pipelines for rows < 100K
                    self.add_TFIDF_solutions()
        elif 'AUDIO' in self.types_present:
            if self.rows > default_hyperparams.multimedia_threshold:
                self.basic_sol.add_splitter()
                self.rows = default_hyperparams.multimedia_threshold
            self.basic_sol.initialize_solution('AUDIO', self.total_cols, self.metric)
        elif 'VIDEO' in self.types_present:
            if self.rows > default_hyperparams.multimedia_threshold:
                self.basic_sol.add_splitter()
                self.rows = default_hyperparams.multimedia_threshold
            self.basic_sol.initialize_solution('VIDEO', self.total_cols, self.metric)

    def add_TFIDF_solutions(self):
        """
        Add solutions for TFIDF text featurization
        """
        basic_sol = solutiondescription.SolutionDescription(self.problem)
        basic_sol.initialize_solution('TFIDFTEXT', self.total_cols, self.metric)
        self.get_primitive_solutions(basic_sol, self.rows)

    def get_solutions(self, dataset, problem_metric, timeout_in_min):
        """
        Get a list of available solutions(pipelines) for the specified task
        Used by both TA2 in "search" phase and TA2-TA3 API.
        """
        self.metric = problem_metric
        self.timeout_in_min = timeout_in_min

        if self.task_name == 'VERTEXNOMINATION' or self.task_name == 'VERTEXCLASSIFICATION':
            self.task_name = 'VERTEXCLASSIFICATION'
            self.get_vertex_classification_pipelines()
        elif self.task_name == 'COMMUNITYDETECTION':
            self.get_community_detection_pipelines()
        elif self.task_name == 'LINKPREDICTION':
            self.get_link_prediction_pipelines()
        elif self.task_name == 'GRAPHMATCHING':
            self.get_graph_matching_pipelines()
        elif self.task_name == 'CLUSTERING':
            self.get_clustering_pipelines()
        elif self.task_name == 'OBJECTDETECTION':
            self.get_object_detection_pipelines()
        elif self.task_name == 'COLLABORATIVEFILTERING':
            self.get_collaborative_filtering_pipelines()
        elif self.task_name == 'FORECASTING':
            self.get_forecasting_pipelines(dataset)
        elif self.task_name == 'LINKPREDICTIONTIMESERIES':
            self.get_link_prediction_timeseries_pipelines()
        else: # CLASSIFICATION / REGRESSION / SEMISUPERVISED / FORE_REGRESSION 
            # Initialize dataset properties, data types etc. 
            self.create_basic_solutions(dataset)
           
            # Run common steps of solutions before forking out processes for classifiers/regressors
            output_step_index = self.basic_sol.index_denormalize + 3
            if self.task_name == 'REMOTESENSING':
                output_step_index = self.basic_sol.index_denormalize + 5
            if 'AUDIO' in self.types_present:
                output_step_index = self.basic_sol.index_denormalize + 2

            # Run basic solution (1-time pass of pipeline steps of data preprocessing and cache final output)
            if self.basic_sol.splitter_present() == False or complex_types_present(self.types_present) == True:
                try:
                    self.basic_sol.run_basic_solution(inputs=[dataset], output_step = output_step_index)
                except Exception as e:
                    print(e)
                    logging.error(sys.exc_info()[0])
                    self.basic_sol = None
                  
            # Run additional(secondary solution), if any
            if self.addn_sol is not None and (self.addn_sol.splitter_present() == False or 'IMAGE' in self.types_present):
                try:
                    self.addn_sol.run_basic_solution(inputs=[dataset], output_step = output_step_index)
                except Exception as e:
                    print(e)
                    logging.error(sys.exc_info()[0])
                    self.addn_sol = None

            # Add primitives to basic solutions
            if self.task_name == 'CLASSIFICATION' or self.task_name == 'REMOTESENSING' or self.task_name == 'REGRESSION' or self.task_name == 'FORE_REGRESSION':
                for sol in [self.basic_sol, self.addn_sol]:
                    self.get_primitive_solutions(sol, self.rows)
                # Try RPI solutions
                if self.basic_sol is not None and \
                    self.basic_sol.splitter == False and \
                    self.is_multi_column_output(self.basic_sol, output_step_index) is False and \
                    'ROC_AUC' not in self.metric:
                        self.get_rpi_solutions(self.basic_sol.add_floats, self.basic_sol.privileged, self.rows, dataset)
                conditioner_prim = 'd3m.primitives.classification.bagging.SKlearn'
                if self.task_name != 'CLASSIFICATION':
                    conditioner_prim = 'd3m.primitives.regression.bagging.SKlearn'
                pipe = self.get_solution_by_task_name('CONDITIONER', ML_prim=conditioner_prim)
                if self.rows < 1000000 and self.total_cols < 1000 and \
                   self.task_name != 'REMOTESENSING' and \
                   complex_types_present(self.types_present) == False and \
                   'ROC_AUC' not in self.metric: #'FORE_REGRESSION': 
                    self.solutions.append(pipe)
            else:
                # Add primitives for SSL solutions
                self.get_SSL_pipelines(self.rows)
                self.get_ssl_rpi_solutions(self.basic_sol.add_floats, self.basic_sol.privileged, self.rows, dataset)

        return self.solutions

    def is_multi_column_output(self, basic_sol, outputstep):
        """
        Does dataset have multiple outputs?
        """
        if basic_sol.primitives_outputs != None and len(basic_sol.primitives_outputs[outputstep].columns) > 1:
            return True
        return False

    def get_primitive_solutions(self, basic_sol, rows):
        """
        Create multiple pipelines for a task by iterating through different primitives
        Iterate through different ML models (classifiers/regressors).
        Each one is evaluated in a seperate process. 
        """
        if basic_sol is None:
            return 

        if self.task_name == "REGRESSION" or self.task_name == "FORE_REGRESSION":
            listOfSolutions = solution_templates.regressors
        else:
            listOfSolutions = solution_templates.classifiers
        
        total_cols = self.total_cols
        dataframestep = 1
        if basic_sol.splitter_present() == True:
            dataframestep = 2

        if complex_types_present(self.types_present) is True and self.task_name == "CLASSIFICATION":
            listOfSolutions.append('d3m.primitives.classification.bernoulli_naive_bayes.SKlearn')

        outputstep = basic_sol.index_denormalize + 3
        if 'AUDIO' in self.types_present:
            outputstep = basic_sol.index_denormalize + 2
        if self.task_name == 'REMOTESENSING':
            outputstep = basic_sol.index_denormalize + 5
            dataframestep = 3
            listOfSolutions = ['d3m.primitives.classification.linear_svc.SKlearn',
                               'd3m.primitives.classification.logistic_regression.SKlearn',
                               'd3m.primitives.classification.random_forest.SKlearn']
      
        construct_primitive = 'd3m.primitives.data_transformation.construct_predictions.Common' 
        if 'ROC_AUC' in self.metric:
            construct_primitive='d3m.primitives.data_transformation.construct_confidence.Common'

        if self.total_cols > 30000:
            if self.task_name == "REGRESSION":
                python_path = 'd3m.primitives.regression.random_forest.SKlearn'
            else:
                python_path = 'd3m.primitives.classification.random_forest.SKlearn'
            basic_sol.add_step(python_path, outputstep = outputstep, dataframestep=dataframestep, construct_primitive=construct_primitive)
            self.solutions.append(basic_sol)
            return

        # Iterate through different primitives (classifiers/regressors)
        for python_path in listOfSolutions:
            # Prune out expensive pipelines
            valid = is_primitive_reasonable(python_path, rows, total_cols, self.types_present, self.task_name, self.metric)
            if valid is False: 
                continue

            if self.is_multi_column_output(basic_sol, outputstep) is True: # multi-column output?
                # These do not work for multi-column output
                if 'linear_sv' in python_path or 'ada_boost' in python_path or 'lasso_cv' in python_path or 'gradient_boosting' in python_path:
                    continue

            # Create new solution by copying basic_sol and appending model.
            # Useful because basic_sol has performed common steps and outputs are cached! 
            pipe = copy.deepcopy(basic_sol)
            pipe.id = str(uuid.uuid4())
            pipe.add_step(python_path, outputstep = outputstep, dataframestep=dataframestep, construct_primitive=construct_primitive)
            self.solutions.append(pipe)

    def get_solution_by_task_name(self, name, ML_prim=None, outputstep=3, dataframestep=1):
        """
        Get a single complete pipeline by task name.
        Used for less frequent tasks (not Classification or regression). 
        name: Name of pipeline template
        ML_prim: ML primitive to be appended (classifier/regressor mostly)
        outputstep: Step in pipeline producing targets
        dataframestep: Dataframe step in pipeline. Used for constructing predictions.
        """
        pipe = solutiondescription.SolutionDescription(self.problem)
        pipe.initialize_solution(name)
        pipe.id = str(uuid.uuid4())
        if ML_prim is not None:
            step1 = pipe.index_denormalize + outputstep
            step2 = pipe.index_denormalize + dataframestep
            pipe.add_step(ML_prim, outputstep=step1, dataframestep=step2)
        else:
            pipe.add_outputs()
        return pipe    

    def get_ssl_rpi_solutions(self, add_floats, privileged, rows, dataset):
        """
        Get RPI-based pipelines for SSL tasks.
        """
        if self.types_present is None:
            return

        if 'AUDIO' in self.types_present or \
           'VIDEO' in self.types_present or \
           'TIMESERIES' in self.types_present or \
           'IMAGE' in self.types_present or \
           'COREXTEXT' in self.types_present:
            return

        basic_sol = solutiondescription.SolutionDescription(self.problem)
        basic_sol.set_privileged(privileged)
        basic_sol.set_add_floats(add_floats)
        basic_sol.initialize_RPI_solution('NOTUNE_PIPELINE_RPI')
        outputstep = basic_sol.index_denormalize + 4
        if add_floats is not None and len(add_floats) > 0:
            outputstep = basic_sol.index_denormalize + 5

        sslVariants = solution_templates.sslVariants
        total_cols = self.total_cols
        if rows <= 100000:
            try:
                basic_sol.run_basic_solution(inputs=[dataset], output_step=outputstep, dataframe_step=basic_sol.index_denormalize + 1)
                total_cols = basic_sol.get_total_cols()
                logging.info("Total cols = %s", total_cols)
            except Exception as e:
                print(e)
                logging.error(sys.exc_info()[0])
                basic_sol = None
        else:
            sslVariants = ['d3m.primitives.classification.random_forest.SKlearn',
                           'd3m.primitives.classification.bagging.SKlearn']

        if basic_sol is None or total_cols > 200:
            return

        # Iterate through different primitives (classifiers)
        for python_path in sslVariants:
            valid = is_primitive_reasonable(python_path, rows, total_cols, self.types_present, self.task_name, self.metric)
            if valid is False:
                continue

            pipe = copy.deepcopy(basic_sol)
            pipe.id = str(uuid.uuid4())
            pipe.add_step('d3m.primitives.semisupervised_classification.iterative_labeling.AutonBox', outputstep = pipe.index_denormalize + 4)
            pipe.add_ssl_variant(python_path)
            self.solutions.append(pipe)

    def get_rpi_solutions(self, add_floats, privileged, rows, dataset):
        """
        Get RPI-based pipelines for classification/regression tasks.
        """
        if self.types_present is None:
            return

        if self.task_name != "REGRESSION" and self.task_name != "CLASSIFICATION":
            return

        if (rows >= 100000 and self.total_cols > 25) or self.total_cols >= 100:
            return

        if 'AUDIO' in self.types_present or \
           'VIDEO' in self.types_present or \
           'TIMESERIES' in self.types_present or \
           'IMAGE' in self.types_present or \
           'COREXTEXT' in self.types_present:
            return

        basic_sol = solutiondescription.SolutionDescription(self.problem)
        basic_sol.set_privileged(privileged)
        basic_sol.set_add_floats(add_floats)
        outputstep = basic_sol.index_denormalize + 4
        if add_floats is not None and len(add_floats) > 0:
            outputstep = basic_sol.index_denormalize + 5

        total_cols = self.total_cols
        if self.task_name == "REGRESSION":
            listOfSolutions = solution_templates.regressors_rpi
        else:
            listOfSolutions = solution_templates.classifiers_rpi

        if rows >= 25000:
            # No tuning
            basic_sol.initialize_RPI_solution('NOTUNE_PIPELINE_RPI')
            if self.task_name == "REGRESSION":
                listOfSolutions = ['d3m.primitives.regression.random_forest.SKlearn']
            else:
                listOfSolutions = ['d3m.primitives.classification.random_forest.SKlearn']
        else:
            # Grid-search over RPI's binsize and model's no. of estimators. This can be expensive
            basic_sol.initialize_RPI_solution('PIPELINE_RPI')
            try:
                basic_sol.run_basic_solution(inputs=[dataset], output_step=outputstep, dataframe_step=basic_sol.index_denormalize + 1)
                total_cols = basic_sol.get_total_cols()
                logging.info("Total cols = %s", total_cols)
            except Exception as e:
                print(e)
                logging.error(sys.exc_info()[0])
                basic_sol = None

        if basic_sol is None or total_cols > 200:
            return

        RPI_steps = ['d3m.primitives.feature_selection.joint_mutual_information.AutoRPI','d3m.primitives.feature_selection.simultaneous_markov_blanket.AutoRPI']

        # Iterate through different primitives (classifiers/regressors)
        for python_path in listOfSolutions:
            # Avoid expensive solutions!!!
            if 'gradient_boosting' in python_path and ((rows > 1000 and total_cols > 50) or (rows > 5000) or total_cols > 100):
                continue

            if rows >= 25000:
                pipe = copy.deepcopy(basic_sol)
                pipe.id = str(uuid.uuid4())
                pipe.add_step(python_path, outputstep)
                self.solutions.append(pipe)
            else:
                for step in RPI_steps:
                    pipe = copy.deepcopy(basic_sol)
                    pipe.id = str(uuid.uuid4())
                    pipe.add_RPI_step(step, python_path, outputstep)
                    self.solutions.append(pipe)

