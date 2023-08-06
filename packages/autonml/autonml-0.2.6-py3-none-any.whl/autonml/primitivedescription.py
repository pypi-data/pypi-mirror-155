                    
# File: primitivedescription.py 
# Author(s): Saswati Ray
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import pandas as pd
import numpy as np
import math, sys
from sklearn import metrics, preprocessing
import logging
import d3m.index
from timeit import default_timer as timer
import operator, traceback
import d3m.metadata.base as metadata_base
from d3m import container

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesClassifier, ExtraTreesRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.ensemble.bagging import BaggingClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression, Lasso, Ridge
from sklearn.linear_model.stochastic_gradient import SGDClassifier
from sklearn.svm import LinearSVC, LinearSVR, SVC, SVR
from sklearn.model_selection import GridSearchCV

# AutonML imports
import autonml.util as util
from autonml.helper_functions import get_split_indices, get_num_splits

gridsearch_estimators_parameters = {'d3m.primitives.regression.random_forest.SKlearn': [RandomForestRegressor(), 
                                                                                        {'n_estimators': [100],
                                                                                         'max_depth': [8, 10, 15, None],
                                                                                         'min_samples_split': [2, 5, 10]}],
              'd3m.primitives.classification.random_forest.SKlearn': [RandomForestClassifier(),
                                                                      {'n_estimators': [100],
                                                                       'max_depth': [8, 10, 15, None],
                                                                       'min_samples_split': [2, 5, 10],
                                                                       'class_weight': ['balanced', None]}],
              'd3m.primitives.classification.extra_trees.SKlearn': [ExtraTreesClassifier(),
                                                                      {'n_estimators': [100],
                                                                       'max_depth': [8, 10, 15, None],
                                                                       'min_samples_split': [2, 5, 10],
                                                                       'class_weight': ['balanced', None]}],
              'd3m.primitives.regression.extra_trees.SKlearn': [ExtraTreesRegressor(),
                                                                      {'n_estimators': [100],
                                                                       'max_depth': [8, 10, 15, None],
                                                                       'min_samples_split': [2, 5, 10]}],
              'd3m.primitives.classification.gradient_boosting.SKlearn': [GradientBoostingClassifier(),
                                                                          {'n_estimators': [100],
                                                                           'max_depth': [3, 5, 8, 10, 15],
                                                                           'max_features': ['sqrt', None],
                                                                           'min_samples_leaf': [1, 2, 5],
                                                                           'min_samples_split': [2, 5, 10]}],
              'd3m.primitives.regression.gradient_boosting.SKlearn': [GradientBoostingRegressor(),
                                                                      {'n_estimators': [100],
                                                                       'max_depth': [3, 5, 8, 10, 15],
                                                                       'max_features': ['sqrt', None],
                                                                       'min_samples_leaf': [1, 2, 5],
                                                                       'min_samples_split': [2, 5, 10]}],
              'd3m.primitives.classification.linear_svc.SKlearn': [LinearSVC(),
                                                                   {'C': [0.01, 0.1, 1, 10, 100],
                                                                    'class_weight': ['balanced', None]}],
              'd3m.primitives.regression.linear_svr.SKlearn': [LinearSVR(),
                                                                   {'C': [0.01, 0.1, 1, 10, 100]}],
              'd3m.primitives.classification.svc.SKlearn': [SVC(),
                                                            {'C': [0.01, 0.1, 1, 10, 100],
                                                             'class_weight': ['balanced', None]}],
              'd3m.primitives.regression.svr.SKlearn': [SVR(),
                                                        {'C': [0.01, 0.1, 1, 10, 100]}],
              'd3m.primitives.classification.logistic_regression.SKlearn': [LogisticRegression(),
                                                                            {'C': [0.1, 1, 10, 100],
                                                                             'class_weight': ['balanced', None]}],
              'd3m.primitives.regression.ridge.SKlearn': [Ridge(), 
                                                          {'alpha': [0.001, 0.01, 0.1, 1, 5]}],
              'd3m.primitives.regression.lasso.SKlearn': [Lasso(),
                                                          {'alpha': [0.001, 0.01, 0.1, 1, 5]}]
}

def rmse(y_true, y_pred):
    return math.sqrt(metrics.mean_squared_error(y_true, y_pred))

def compute_min_class(y, pos_label):
    frequencies = y.iloc[:,0].value_counts(normalize=True)
    min_freq = frequencies.iat[len(frequencies)-1]
    return min_freq

class PrimitiveDescription(object):
    """
    Class representing single primitive.
    Used for optimizing primitive hyper-parameters, doing cross-validation.
    """
    def __init__(self, primitive, primitive_class):
        self.id = primitive_class.id
        self.primitive = primitive
        self.primitive_class = primitive_class

    def score_ESRNN_primitive(self, prim_instance, X, y):
        """
        ESRNN evaluation! 
        Can only do MAE metric (as yet)!
        Retrieve internal CV score
        """
        prim_instance.set_training_data(inputs=X, outputs=y)
        prim_instance.fit()
        try:
            metric = min(prim_instance._esrnn.losses)
        except:
            metric = 0

        return metric

    def create_optimal_parameters(self, X):
        optimal_params = dict()
        python_path = self.primitive.metadata.query()['python_path']

        # Put constraints on primitive hyperparameters to avoid excessive time-complexity!
        if 'SKlearn' in python_path:
            hyperparam_spec = self.primitive.metadata.query()['primitive_code']['hyperparams']
            if len(X) >= 50000 and ('random_forest' in python_path or 'gradient_boosting' in python_path or 'bagging' in python_path): # 'n_estimators' in hyperparam_spec:
                optimal_params['n_estimators'] = 50
            if len(X) >= 100000 and 'n_estimators' in hyperparam_spec:
                optimal_params['n_estimators'] = 10
            if (len(X) >= 100000 or len(X.columns) >= 5000) and ('linear_svc' in python_path or 'linear_svr' in python_path):
                optimal_params['max_iter'] = 100
            if len(X.columns) > 500 and ('bagging' in python_path):
                optimal_params['max_features'] = 15
            if len(X.columns) > 50 and 'gradient_boosting' in python_path:
                optimal_params['max_features'] = 7
            if len(X.columns) >= 5000 and ('random_forest' in python_path or 'extra_trees' in python_path):
                optimal_params['max_features'] = 30
        return optimal_params 
 
    def score_primitive(self, X, y, metric_type, posLabel, custom_hyperparams, taskname, pipeline_id=None, mode=None):
        """
        Learns optimal hyperparameters for the primitive
        Returns metric score and optimal parameters.
        X: Training data inputs
        y: Training data outputs
        metric_type: Scoring metric
        posLabel: Positive label for F1 metric
        """
        python_path = self.primitive.metadata.query()['python_path']

        optimal_params = self.create_optimal_parameters(X)

        if custom_hyperparams is not None:
            for name, value in custom_hyperparams.items():
                optimal_params[name] = value

        # No CV for these primitives!
        if X is None or y is None or 'graph' in python_path or 'Vertex' in python_path or \
            'DistilLink' in python_path or \
            'community' in python_path or \
            'JHU' in python_path or \
            'yolo' in python_path or \
            'FCN' in python_path or \
            'retina' in python_path:
            if util.invert_metric(metric_type) is True:
                return (0.0, optimal_params)
            else:
                if 'JHU' in python_path:
                    return (0.99, optimal_params)
                if 'retina' in python_path:
                    return (0.99, optimal_params)
                return (1.0, optimal_params)

        # Lasso CV can become very expensive for large number of columns!!!
        # Use lasso's CV score
        if 'lasso_cv' in python_path and len(X.columns) > 500:
            return (1.0, optimal_params)

        primitive_hyperparams = self.primitive.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
        prim_instance = self.primitive(hyperparams=primitive_hyperparams(primitive_hyperparams.defaults(), **optimal_params))
        score = 0.0

        # ESRNN evaluation! 
        # Can only do MAE metric (as yet)!
        # Retrieve internal CV score
        if 'esrnn' in python_path:
            start = timer()
            score = self.score_ESRNN_primitive(prim_instance, X, y)
            end = timer()
            if mode is not None:
                try:
                    predictions = prim_instance.produce(X)
                    outputFilePath = mode + "/" + str(pipeline_id) + "_train_predictions.csv"
                    with open(outputFilePath, 'w') as outputFile:
                        predictions.to_csv(outputFile, header=True)
                except:
                    predictions = None
                    
            logging.critical("Time taken for esrnn = %s secs", end-start) 
            logging.critical("MAE Score for %s = %s", python_path, score)
            return (score, optimal_params)

        splits = get_num_splits(len(X), len(X.columns))
        
        # Hard coding MAE for forecasting problems since thats what esrnn supports!
        if taskname == 'FORE_REGRESSION' or 'FORECASTING' in taskname:
            metric_type = "MEAN_ABSOLUTE_ERROR"

        logging.critical("%s - %s - %s", python_path, X.shape, optimal_params)
        # Run k-fold CV and compute mean metric score 
        (score, metric_scores) = self.k_fold_CV(prim_instance, X, y, metric_type, posLabel, splits, pipeline_id, mode)
        return (score, optimal_params)

    def score_array(self, X, X2, y, y2, metric_type, posLabel, custom_hyperparams, taskname, pipeline_id=None, mode=None):
        """
        Score a primitive using given train-test splits
        X: Train splits
        X2: Test splits
        y: Train output splits
        y2: Test output splits
        """
        #breakpoint()
        python_path = self.primitive.metadata.query()['python_path']
        optimal_params = self.create_optimal_parameters(X[0])

        if custom_hyperparams is not None:
            for name, value in custom_hyperparams.items():
                optimal_params[name] = value

        if 'lasso_cv' in python_path and len(X[0].columns) > 500:
            return (1.0, optimal_params)

        primitive_hyperparams = self.primitive.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
        prim_instance = self.primitive(hyperparams=primitive_hyperparams(primitive_hyperparams.defaults(), **optimal_params))
        score = 0.0

        for X_train, y_train, X_test, y_test in zip(X, y, X2, y2):
            prim_instance.set_training_data(inputs=X_train, outputs=y_train)
            prim_instance.fit()
            predictions = prim_instance.produce(inputs=X_test).value
            if 'xgboost' in python_path and len(predictions.columns) > 1:
                predictions = predictions.iloc[:,len(predictions.columns)-1]

            metric = self.evaluate_metric(predictions, y_test, metric_type, posLabel)
            score += metric
        logging.critical("%s - %s - %s", python_path, X[0].shape, optimal_params)
        score /= len(X)
        return (score, optimal_params)

    def evaluate_metric(self, predictions, Ytest, metric, posLabel):
        """
        Function to compute metric score for predicted-vs-true output.
        """
        count = len(Ytest)

        if metric == "ACCURACY":
            return metrics.accuracy_score(Ytest, predictions)
        elif metric == "PRECISION":
            return metrics.precision_score(Ytest, predictions)
        elif metric == "RECALL":
            return metrics.recall_score(Ytest, predictions)
        elif metric == "F1":
            return metrics.f1_score(Ytest, predictions, pos_label=posLabel)
        elif metric == "F1_MICRO":
            return metrics.f1_score(Ytest, predictions, average='micro')
        elif metric == "F1_MACRO":
            return metrics.f1_score(Ytest, predictions, average='macro')
        elif metric == "ROC_AUC":
            return metrics.roc_auc_score(Ytest, predictions, multi_class='ovr')
        elif metric == "ROC_AUC_MICRO":
            return metrics.roc_auc_score(Ytest, predictions, multi_class='ovr', average='micro')
        elif metric == "ROC_AUC_MACRO":
            return metrics.roc_auc_score(Ytest, predictions, multi_class='ovr', average='macro')
        elif metric == "MEAN_SQUARED_ERROR":
            return metrics.mean_squared_error(Ytest, predictions)
        elif metric == "ROOT_MEAN_SQUARED_ERROR":
            return math.sqrt(metrics.mean_squared_error(Ytest, predictions))
        elif metric == "MEAN_ABSOLUTE_ERROR":
            return metrics.mean_absolute_error(Ytest, predictions)
        elif metric == "R_SQUARED":
            return metrics.r2_score(Ytest, predictions)
        elif metric == "NORMALIZED_MUTUAL_INFORMATION":
            return metrics.normalized_mutual_info_score(Ytest, predictions)
        elif metric == "JACCARD_SIMILARITY_SCORE":
            return metrics.jaccard_similarity_score(Ytest, predictions)
        elif metric == "PRECISION_AT_TOP_K":
            return 0.0
        elif metric == "OBJECT_DETECTION_AVERAGE_PRECISION":
            return 0.0
        elif metric == "MEAN_RECIPROCAL_RANK":
            return 0.0
        elif metric == "HITS_AT_K":
            return 0.0
        else:
            return metrics.accuracy_score(Ytest, predictions)

    def optimize_primitive_gridsearch(self, train, output, python_path, metric, posLabel):
        # Do grid-search to learn optimal parameters for the model
        if python_path in gridsearch_estimators_parameters:
            start = timer()
            (model, search_grid) = gridsearch_estimators_parameters[python_path]
            splits = get_num_splits(len(train), len(train.columns))

            from sklearn.metrics import make_scorer
            if metric == "ACCURACY":
                scorer = make_scorer(metrics.accuracy_score)
            elif metric == "F1":
                scorer = make_scorer(metrics.f1_score, pos_label=posLabel)
            elif metric == "F1_MACRO":
                scorer = make_scorer(metrics.f1_score, average='macro')
            elif metric == "MEAN_SQUARED_ERROR":
                scorer = make_scorer(metrics.mean_squared_error, greater_is_better=False)
            elif metric == "ROOT_MEAN_SQUARED_ERROR": 
                scorer = make_scorer(rmse, greater_is_better=False)
            else:
                scorer = None

            rf_random = GridSearchCV(estimator = model, param_grid = search_grid, scoring = scorer, cv = splits, verbose=0, n_jobs = -1)

            # Fit the random search model
            rf_random.fit(train, output)
            print(rf_random.best_params_)
            end = timer() 
            print("Time taken for ", python_path, " = ", end-start, " secs")
            return rf_random.best_params_
        else:
            print("No grid search done for ", python_path)
            return None

    def optimize_F1_metric(self, train, y, optimal_params, metric_type, posLabel):
        corex_hp = {'class_weight': ['balanced', None]}

        RPI_path = self.primitive.metadata.query()['python_path']
        primitive_hyperparams = self.primitive.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']

        splits = get_num_splits(len(train), len(train.columns))
        scores = {}

        start = timer()
        for i in corex_hp['class_weight']:
            optimal_params['class_weight'] = i
            model = self.primitive(hyperparams=primitive_hyperparams(primitive_hyperparams.defaults(), **optimal_params))
            (score, metric_scores) = self.k_fold_CV(model, train, y, metric_type, posLabel, splits)
            mean = np.mean(metric_scores)
            scores[(i,mean)] = mean
        print(RPI_path)
        print(scores)
        sorted_x = sorted(scores.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        (key, value) = sorted_x[0]
        end = timer()
        logging.critical("%s time taken = %s secs", RPI_path, end-start)
        return key

    def optimize_RPI_bins(self, train, y, python_path, metric_type, posLabel):
        corex_hp = {'nbins': [2, 3, 4, 10],# 12, 15, 20],
                    'method': ['counting', 'fullBayesian'], #'pseudoBayesian'],
                    'n_estimators': [20, 25, 30, 32]}
   
        RPI_path = self.primitive.metadata.query()['python_path'] 
        # For simultaneous_markov_blanket.AutoRPI
        if 'markov' in RPI_path:
            corex_hp['nbins'] = [10]
            corex_hp['method'] = ['counting']#, 'pseudoBayesian', 'fullBayesian', 'BayesFactor']

        if(len(train) > 25000): # Use defaults. No tuning
            corex_hp = {'nbins': [10],
                        'method': ['counting'],
                        'n_estimators': [10]}

        if 'linear_discriminant_analysis' in python_path:
            corex_hp['n_estimators'] = [0]

        prim = d3m.index.get_primitive(python_path)
        model_hyperparams = prim.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']

        primitive_hyperparams = self.primitive.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']

        sklearn_prim = d3m.index.get_primitive('d3m.primitives.data_cleaning.imputer.SKlearn')
        sklearn_hyperparams = sklearn_prim.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
        custom_hyperparams = dict()
        custom_hyperparams['strategy'] = 'most_frequent'
        sklearn_primitive = sklearn_prim(hyperparams=sklearn_hyperparams(sklearn_hyperparams.defaults(), **custom_hyperparams))

        splits = get_num_splits(len(train), len(train.columns))
        scores = {}

        start = timer()

        for i in corex_hp['nbins']:
            custom_hyperparams = dict()
            custom_hyperparams['nbins'] = i

            for j in corex_hp['method']:
                custom_hyperparams['method'] = j
                model = self.primitive(hyperparams=primitive_hyperparams(primitive_hyperparams.defaults(), **custom_hyperparams))

                model.set_training_data(inputs=train, outputs=y)
                model.fit()
                output = model.produce(inputs=train).value

                sklearn_primitive.set_training_data(inputs=output)
                sklearn_primitive.fit()
                output = sklearn_primitive.produce(inputs=output).value

                for k in corex_hp['n_estimators']:
                    model_hp = dict()
                    model_hp['n_estimators'] = k
                    if 'gradient_boosting' in python_path:
                        model_hp['learning_rate'] = 10/k
                    if 'linear_discriminant_analysis' in python_path:
                        rf_model = prim(hyperparams=model_hyperparams(model_hyperparams.defaults()))
                    else:
                        rf_model = prim(hyperparams=model_hyperparams(model_hyperparams.defaults(), **model_hp))
                    (score, metric_scores) = self.k_fold_CV(rf_model, output, y, metric_type, posLabel, splits)
                    mean = np.mean(metric_scores)
                    median = np.median(metric_scores)
                    stderror = np.std(metric_scores)/math.sqrt(len(metric_scores))
                    z = 1.96*stderror
                    scores[(i,j,k,mean)] = mean#-z

        sorted_x = sorted(scores.items(), key=operator.itemgetter(1))
        if util.invert_metric(metric_type) is False:
            sorted_x.reverse()
        (key, value) = sorted_x[0]
        end = timer()
        logging.critical("%s time taken for %s = %s secs", RPI_path, python_path, end-start)
        return key

    def k_fold_CV(self, prim_instance, X, y, metric_type, posLabel, splits, pipeline_id=None, mode=None):
        """
        Run k-fold CV.
        k = splits
        prim_instance has already been initialized with hyperparameters.
        """
        python_path = self.primitive.metadata.query()['python_path']
        metric_sum = 0
        score = 0.0

        if 'NBEATS' in python_path:
            metric = 5000
            return (metric, [metric, metric])
        if 'VAR' in python_path or 'arima' in python_path or 'nbeats' in python_path:
            start = timer()
            prim_instance.set_training_data(inputs=X, outputs=y)
            prim_instance.fit()
            predictions = prim_instance.produce(inputs=X).value
            predictions = predictions.iloc[:,len(predictions.columns)-1]
            if mode is not None:
                outputFilePath = mode + "/" + str(pipeline_id) + "_train_predictions.csv"
                with open(outputFilePath, 'w') as outputFile:
                    predictions.to_csv(outputFile, header=True)
            metric = self.evaluate_metric(predictions, y, metric_type, posLabel)
            end = timer()
            logging.critical("Time taken for %s = %s secs (%f)", python_path, end-start, metric)
            return (metric, [metric, metric])

        # Run k-fold CV and compute mean metric score
        metric_scores = []
        split_indices = get_split_indices(X, y, splits, python_path)

        start = timer()
        train_predictions = None

        if mode is not None:
            # Create training predictions
            train_predictions = pd.DataFrame(columns=["Prediction"], index=np.arange(len(X)))
            if "ROC_AUC" in metric_type:
                labels = sorted(y.iloc[:,0].unique())
                if labels[0] == '':
                    labels = labels[1:]
                num_classes = len(labels) 
                train_predictions = pd.DataFrame(columns=["Prediction"], index=np.repeat(np.arange(len(X)),num_classes))

        # Do the actual k-fold CV here
        for train_index, test_index in split_indices:
            X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
            y_train, y_test = y.iloc[train_index,:], y.iloc[test_index,:]

            X_test.reset_index(drop=True,inplace=True)
            prim_instance.set_training_data(inputs=X_train, outputs=y_train)
            prim_instance.fit()

            # Compute predictions on test data
            if "ROC_AUC" in metric_type:
                input_labels = container.DataFrame(labels)
                input_labels = input_labels.append([input_labels] * (len(y_test) - 1)).reset_index(drop=True)
                input_labels.metadata = input_labels.metadata.generate(input_labels)
                input_labels.metadata = input_labels.metadata.add_semantic_type((metadata_base.ALL_ELEMENTS, 0), 'https://metadata.datadrivendiscovery.org/types/TrueTarget')
                primitive_inputs = X_test.loc[X_test.index.repeat(len(labels))].reset_index(drop=True)
                primitive_inputs.metadata = X_test.metadata.update((), {'dimension': {'length': len(labels)}})
                predictions = prim_instance.log_likelihoods(inputs=primitive_inputs,outputs=input_labels).value
                predictions = predictions.apply(np.vectorize(np.exp))
            else:
                predictions = prim_instance.produce(inputs=X_test).value

            if ('xgboost' in python_path or 'DeepAR' in python_path) and len(predictions.columns) > 1:
                predictions = predictions.iloc[:,len(predictions.columns)-1]

            # Compute evaluation metric on test set 
            try:
                if "ROC_AUC" in metric_type:
                    indices = [np.arange(i*num_classes, i*num_classes+num_classes) for i in test_index]
                    indices = np.ravel(indices)
                    train_predictions.iloc[indices] = predictions.values
                    output = predictions.groupby(np.arange(len(predictions)) // num_classes, as_index=False).aggregate(lambda x: tuple(v for v in x))
                    output.reset_index(inplace=True)
                    output.drop(columns='index',inplace=True)
                    encoded = output.iloc[:,0].apply(pd.Series)
                    encoded.columns = labels
                    if len(labels) == 2:
                        encoded = encoded.iloc[:,1]
                    predictions = encoded.to_numpy()
                    y_test = np.squeeze(y_test.values)
                    if 'iterative_labeling' in python_path: # Semi-supervised ?
                        labeledIx = np.where(y_test[:] != '')[0]
                        predictions = predictions[labeledIx]
                        y_test = y_test[labeledIx]
                elif 'iterative_labeling' in python_path: # Semi-supervised ?
                    labeledIx = np.where(y_test.iloc[:, 0].values != '')[0]
                    predictions = predictions.iloc[labeledIx]
                    y_test = y_test.iloc[labeledIx]  
                metric = self.evaluate_metric(predictions, y_test, metric_type, posLabel)
            except:
                metric = 0

            if train_predictions is not None and "ROC_AUC" not in metric_type:
                if 'xgboost' in python_path:
                    train_predictions.loc[test_index, :] = predictions.values.reshape(-1, 1)
                else:
                    train_predictions.loc[test_index, :] = predictions.values

            metric_scores.append(metric)
            metric_sum += metric

        if train_predictions is not None:
            outputFilePath = mode + "/" + str(pipeline_id) + "_train_predictions.csv"
            with open(outputFilePath, 'w') as outputFile:
                train_predictions.to_csv(outputFile, header=True)

        score = metric_sum/splits
        end = timer()
        if 'RPI' not in python_path:
            logging.critical("Time taken for %s = %s secs (%f)", python_path, end-start, score)
        return (score, metric_scores)
