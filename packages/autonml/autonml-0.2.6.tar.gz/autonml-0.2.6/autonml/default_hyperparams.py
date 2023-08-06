
# File: default_hyperparams.py 
# Author(s): Saswati Ray
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

__version__ = "0.1.0"

import os, json
import pandas as pd
import numpy as np

multimedia_threshold = 1200

def set_default_hyperparameters(path, taskname):
    """     
    Retrieve the default hyperparameters to be set for a primitive.
    Parameters     ---------     
    path: Python path of a primitive
    """

    hyperparams = None
    # Set hyperparameters for specific primitives
    if path == 'd3m.primitives.data_cleaning.imputer.SKlearn':
        hyperparams = {}
        hyperparams['use_semantic_types'] = True
        hyperparams['return_result'] = 'replace'
        hyperparams['strategy'] = 'median'
        hyperparams['error_on_no_input'] = False

    if path == 'd3m.primitives.data_transformation.one_hot_encoder.SKlearn':
        hyperparams = {}
        hyperparams['use_semantic_types'] = True
        hyperparams['return_result'] = 'replace'
        hyperparams['handle_unknown'] = 'ignore'

    if path == 'd3m.primitives.data_cleaning.robust_scaler.SKlearn':
        hyperparams = {}
        hyperparams['return_result'] = 'replace'

    if path == 'd3m.primitives.feature_construction.corex_text.DSBOX':
        hyperparams = {}
        hyperparams['threshold'] = 500

    if 'conditioner' in path:
        hyperparams = {}
        hyperparams['ensure_numeric'] = True
        hyperparams['maximum_expansion'] = 30

    if path == 'd3m.primitives.clustering.k_means.Fastlvm':
        hyperparams = {}
        hyperparams['k'] = 100

    if 'adjacency_spectral_embedding.JHU' in path:
        hyperparams = {}
        hyperparams['max_dimension'] = 5
        hyperparams['use_attributes'] = True
        if 'LINK' in taskname:
            hyperparams['max_dimension'] = 2
            hyperparams['use_attributes'] = False
            hyperparams['which_elbow'] = 1

    if 'splitter' in path:
        hyperparams = {}
        if taskname == 'IMAGE' or taskname == 'IMAGE2' or taskname == 'AUDIO' or taskname == 'VIDEO':
            hyperparams['threshold_row_length'] = multimedia_threshold
        else:
            hyperparams['threshold_row_length'] = 100000

    if path == 'd3m.primitives.link_prediction.link_prediction.DistilLinkPrediction':
        hyperparams = {}
        hyperparams['metric'] = 'accuracy'

    if path == 'd3m.primitives.vertex_nomination.seeded_graph_matching.DistilVertexNomination':
        hyperparams = {}
        hyperparams['metric'] = 'accuracy'

    if path == 'd3m.primitives.graph_matching.seeded_graph_matching.DistilSeededGraphMatcher':
        hyperparams = {}
        hyperparams['metric'] = 'accuracy'

    if 'PCA' in path:
        hyperparams = {}
        hyperparams['n_components'] = 10

    if path == 'd3m.primitives.data_transformation.image_reader.Common':
        hyperparams = {}
        hyperparams['use_columns'] = [0,1]
        hyperparams['return_result'] = 'replace'

    if path == 'd3m.primitives.data_transformation.text_reader.Common':
        hyperparams = {}
        hyperparams['return_result'] = 'replace'

    if path == 'd3m.primitives.time_series_forecasting.arima.DSBOX':
        hyperparams = {}
        hyperparams['take_log'] = False

    if path == 'd3m.primitives.time_series_forecasting.lstm.DeepAR':
        hyperparams = {}
        hyperparams['epochs'] = 3

    if path == 'd3m.primitives.graph_clustering.gaussian_clustering.JHU':
        hyperparams = {}
        hyperparams['max_clusters'] = 10 

    if path == 'd3m.primitives.time_series_forecasting.esrnn.RNN':
        hyperparams = {}
        hyperparams['auto_tune'] = True
        hyperparams['output_size'] = 60

    if path == 'd3m.primitives.time_series_forecasting.nbeats.DeepNeuralNetwork':
        hyperparams = {}
        hyperparams['loss'] = "MSE"
        hyperparams['seasonality'] = 24
        hyperparams['lr_decay'] = 0.5
        hyperparams['window_sampling_limit_multiplier'] = 200
        hyperparams['batch_size'] = 8

    if 'NBEATS' in path:
        hyperparams = {}
        hyperparams['prediction_length'] = 21
        hyperparams['num_context_lengths'] = 1
        hyperparams['output_mean'] = False

    if 'satellite_image_loader' in path:
        hyperparams = {}
        hyperparams['return_result'] = 'replace'

    if 'tfidf' in path:
        hyperparams = {}
        hyperparams['return_result'] = 'replace'
        hyperparams['use_semantic_types'] = True
        hyperparams['min_df'] = 0.025
        hyperparams['max_df'] = 0.85
        hyperparams['stop_words'] = 'english'

    if 'pca' in path:
        hyperparams = {}
        hyperparams['n_components'] = 10
        hyperparams['return_result'] = 'replace'

    if 'remote_sensing' in path:
        hyperparams = {}
        hyperparams['batch_size'] = 128
        hyperparams['pool_features'] = False

    if 'gcn_mixhop' in path:
        hyperparams = {}
        hyperparams['epochs'] = 200

    return hyperparams
