
# File: solution_templates.py 
# Author(s): Saswati Ray
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import os, sys

task_paths = {
'DISTILTEXT': ['d3m.primitives.data_transformation.denormalize.Common',
               'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
               'd3m.primitives.schema_discovery.profiler.Common',
               'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
               'd3m.primitives.data_transformation.column_parser.Common',
               'd3m.primitives.data_transformation.text_reader.Common',
               'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
               'd3m.primitives.data_cleaning.imputer.SKlearn',
               'd3m.primitives.data_transformation.encoder.DistilTextEncoder'],

'TFIDFTEXT': ['d3m.primitives.data_transformation.denormalize.Common',
               'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
               'd3m.primitives.schema_discovery.profiler.Common',
               'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
               'd3m.primitives.data_transformation.column_parser.Common',
               'd3m.primitives.data_transformation.text_reader.Common',
               'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
               'd3m.primitives.data_cleaning.imputer.SKlearn',
               'd3m.primitives.feature_extraction.tfidf_vectorizer.SKlearn'],

'COREXTEXT': ['d3m.primitives.data_transformation.denormalize.Common',
              'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
              'd3m.primitives.schema_discovery.profiler.Common',
              'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
              'd3m.primitives.data_transformation.column_parser.Common',
              'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
              'd3m.primitives.data_cleaning.imputer.SKlearn',
              'd3m.primitives.feature_construction.corex_text.DSBOX'],

'TIMESERIES': ['d3m.primitives.data_transformation.denormalize.Common',
               'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
               'd3m.primitives.schema_discovery.profiler.Common',
               'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
               'd3m.primitives.data_transformation.time_series_to_list.DSBOX',
               'd3m.primitives.feature_extraction.random_projection_timeseries_featurization.DSBOX',
               'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common'],

'TIMESERIES2': ['d3m.primitives.data_transformation.time_series_formatter.DistilTimeSeriesFormatter',
                'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common'],

'TIMESERIES3': ['d3m.primitives.data_transformation.denormalize.Common',
                'd3m.primitives.time_series_classification.convolutional_neural_net.LSTM_FCN'],

'ISI_PIPELINE': ['d3m.primitives.data_transformation.denormalize.Common',
                 'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                 'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                 'd3m.primitives.feature_construction.gcn_mixhop.DSBOX'],

'IMAGE2': ['d3m.primitives.data_transformation.denormalize.Common',
           'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
           'd3m.primitives.schema_discovery.profiler.Common',
           'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
           'd3m.primitives.data_transformation.dataframe_to_tensor.DSBOX',
           'd3m.primitives.feature_extraction.resnet50_image_feature.DSBOX'],

'IMAGE': ['d3m.primitives.data_transformation.denormalize.Common',
          'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
          'd3m.primitives.schema_discovery.profiler.Common',
          'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
          'd3m.primitives.data_transformation.image_reader.Common',
          'd3m.primitives.data_transformation.column_parser.Common',
          'd3m.primitives.feature_extraction.image_transfer.DistilImageTransfer'],

'VIDEO': ['d3m.primitives.data_transformation.denormalize.Common',
          'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
          'd3m.primitives.schema_discovery.profiler.Common',
          'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
          'd3m.primitives.data_transformation.column_parser.Common',
          'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
          'd3m.primitives.feature_extraction.resnext101_kinetics_video_features.VideoFeaturizer'],

'CLASSIFICATION': ['d3m.primitives.data_transformation.denormalize.Common',
                   'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                   'd3m.primitives.schema_discovery.profiler.Common',
                   'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                   'd3m.primitives.data_transformation.column_parser.Common',
                   'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                   'd3m.primitives.data_cleaning.imputer.SKlearn'],

'CONDITIONER': ['d3m.primitives.data_transformation.denormalize.Common',
                'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                'd3m.primitives.schema_discovery.profiler.Common',
                'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                'd3m.primitives.data_transformation.column_parser.Common',
                'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                'd3m.primitives.data_transformation.conditioner.Conditioner',
                'd3m.primitives.feature_extraction.feature_agglomeration.SKlearn'],

'SEMISUPERVISED': ['d3m.primitives.data_transformation.denormalize.Common',
                   'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                   'd3m.primitives.schema_discovery.profiler.Common',
                   'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                   'd3m.primitives.data_transformation.column_parser.Common',
                   'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                   'd3m.primitives.data_cleaning.imputer.SKlearn'],

'SEMISUPERVISED_HDB': ['d3m.primitives.data_transformation.denormalize.Common',
                       'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                       'd3m.primitives.schema_discovery.profiler.Common',
                       'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                       'd3m.primitives.data_transformation.column_parser.Common',
                       'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                       'd3m.primitives.clustering.hdbscan.Hdbscan',
                       'd3m.primitives.data_cleaning.imputer.SKlearn'],

'ARIMA_FORECASTING': ['d3m.primitives.data_transformation.denormalize.Common',
                      'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                      'd3m.primitives.schema_discovery.profiler.Common',
                      'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                      'd3m.primitives.data_transformation.column_parser.Common',
                      'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                      'd3m.primitives.time_series_forecasting.arima.DSBOX'],

'VAR_FORECASTING': ['d3m.primitives.data_transformation.denormalize.Common',
                    'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                    'd3m.primitives.schema_discovery.profiler.Common',
                    'd3m.primitives.data_transformation.column_parser.Common',
                    'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                    'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                    'd3m.primitives.time_series_forecasting.vector_autoregression.VAR'],

'LSTM_FORECASTING': ['d3m.primitives.data_transformation.denormalize.Common',
                      'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                      'd3m.primitives.schema_discovery.profiler.Common',
                      'd3m.primitives.data_transformation.column_parser.Common',
                      'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                      'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                      'd3m.primitives.time_series_forecasting.lstm.DeepAR'],

'ESRNN_FORECASTING': ['d3m.primitives.data_transformation.denormalize.Common',
                      'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                      'd3m.primitives.schema_discovery.profiler.Common',
                      'd3m.primitives.data_transformation.column_parser.Common',
                      'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                      'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                      'd3m.primitives.data_cleaning.imputer.SKlearn',
                      'd3m.primitives.data_transformation.grouping_field_compose.Common',
                      'd3m.primitives.time_series_forecasting.esrnn.RNN',
                      'd3m.primitives.data_transformation.construct_predictions.Common'],

'NBEATS_FORECASTING': ['d3m.primitives.data_transformation.denormalize.Common',
                       'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                       'd3m.primitives.schema_discovery.profiler.Common',
                       'd3m.primitives.data_transformation.column_parser.Common',
                       'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                       'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                       'd3m.primitives.data_cleaning.imputer.SKlearn',
                       'd3m.primitives.data_transformation.grouping_field_compose.Common',
                       'd3m.primitives.time_series_forecasting.nbeats.DeepNeuralNetwork',
                       'd3m.primitives.data_transformation.construct_predictions.Common'],

'DISTIL_NBEATS': ['d3m.primitives.data_transformation.denormalize.Common',
                  'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                  'd3m.primitives.schema_discovery.profiler.Common',
                  'd3m.primitives.data_transformation.column_parser.Common',
                  'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                  'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                  'd3m.primitives.time_series_forecasting.feed_forward_neural_net.NBEATS',
                  'd3m.primitives.data_transformation.construct_predictions.Common'],

'REGRESSION': ['d3m.primitives.data_transformation.denormalize.Common',
               'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
               'd3m.primitives.schema_discovery.profiler.Common',
               'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
               'd3m.primitives.data_transformation.column_parser.Common',
               'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
               'd3m.primitives.data_cleaning.imputer.SKlearn'],

'FORE_REGRESSION': ['d3m.primitives.data_transformation.denormalize.Common',
                    'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                    'd3m.primitives.schema_discovery.profiler.Common',
                    'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                    'd3m.primitives.data_transformation.column_parser.Common',
                    'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                    'd3m.primitives.data_cleaning.imputer.SKlearn'],

'PIPELINE_RPI': ['d3m.primitives.data_transformation.denormalize.Common',
                 'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                 'd3m.primitives.schema_discovery.profiler.Common',
                 'd3m.primitives.data_transformation.column_parser.Common',
                 'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                 'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common'],

'NOTUNE_PIPELINE_RPI': ['d3m.primitives.data_transformation.denormalize.Common',
                        'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                        'd3m.primitives.schema_discovery.profiler.Common',
                        'd3m.primitives.data_transformation.column_parser.Common',
                        'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                        'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                        'd3m.primitives.feature_selection.joint_mutual_information.AutoRPI',
                        'd3m.primitives.data_cleaning.imputer.SKlearn'],

'CLUSTERING': ['d3m.primitives.data_transformation.dataset_to_dataframe.Common',
               'd3m.primitives.schema_discovery.profiler.Common',
               'd3m.primitives.data_transformation.column_parser.Common',
               'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
               'd3m.primitives.clustering.k_means.Fastlvm',
               'd3m.primitives.data_transformation.construct_predictions.Common'],

'GRAPHMATCHING': ['d3m.primitives.data_transformation.load_graphs.DistilGraphLoader',
                  'd3m.primitives.graph_matching.seeded_graph_matching.DistilSeededGraphMatcher'],

'GRAPHMATCHING2': ['d3m.primitives.graph_matching.seeded_graph_matching.JHU'],

'GRAPHMATCHING3': ['d3m.primitives.data_transformation.dataset_to_dataframe.Common',
                   'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                   'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                   'd3m.primitives.graph_matching.euclidean_nomination.JHU'],

'COLLABORATIVEFILTERING': ['d3m.primitives.data_transformation.denormalize.Common',
                           'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                           'd3m.primitives.schema_discovery.profiler.Common',
                           'd3m.primitives.data_transformation.column_parser.Common',
                           'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                           'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                           'd3m.primitives.collaborative_filtering.link_prediction.DistilCollaborativeFiltering',
                           'd3m.primitives.data_transformation.construct_predictions.Common'],

'VERTEXCLASSIFICATION3': ['d3m.primitives.data_transformation.load_edgelist.DistilEdgeListLoader',
                         'd3m.primitives.vertex_nomination.seeded_graph_matching.DistilVertexNomination'],

'VERTEXCLASSIFICATION2': ['d3m.primitives.data_transformation.load_graphs.JHU',
                          'd3m.primitives.data_preprocessing.largest_connected_component.JHU',
                          'd3m.primitives.data_transformation.adjacency_spectral_embedding.JHU',
                          'd3m.primitives.classification.gaussian_classification.JHU'],

'VERTEXCLASSIFICATION': ['d3m.primitives.data_transformation.load_single_graph.DistilSingleGraphLoader',
                         'd3m.primitives.vertex_nomination.seeded_graph_matching.DistilVertexNomination'],

'OBJECTDETECTION': ['d3m.primitives.data_transformation.denormalize.Common',
                    'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                    'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                    'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
                    'd3m.primitives.feature_extraction.yolo.DSBOX'],

'OBJECTDETECTION2': ['d3m.primitives.data_transformation.denormalize.Common',
                     'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                     'd3m.primitives.object_detection.retina_net.ObjectDetectionRN'],

'LINKPREDICTION2': ['d3m.primitives.link_prediction.data_conversion.JHU', 
                    'd3m.primitives.data_transformation.adjacency_spectral_embedding.JHU',
                    'd3m.primitives.link_prediction.rank_classification.JHU'],

'LINKPREDICTION': ['d3m.primitives.data_transformation.load_single_graph.DistilSingleGraphLoader',
                    'd3m.primitives.link_prediction.link_prediction.DistilLinkPrediction'],

'COMMUNITYDETECTION': ['d3m.primitives.data_transformation.load_single_graph.DistilSingleGraphLoader',
                       'd3m.primitives.community_detection.parser.DistilCommunityDetection'],

'COMMUNITYDETECTION2': ['d3m.primitives.data_transformation.load_graphs.JHU',
	                'd3m.primitives.data_preprocessing.largest_connected_component.JHU',
                        'd3m.primitives.data_transformation.adjacency_spectral_embedding.JHU',
	                'd3m.primitives.graph_clustering.gaussian_clustering.JHU'],

'IMVADIO': ['d3m.primitives.data_transformation.denormalize.Common',
          'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
          'd3m.primitives.schema_discovery.profiler.Common',
          'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
          'd3m.primitives.data_transformation.column_parser.Common',
          'd3m.primitives.data_transformation.text_reader.Common',
          'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',
          'd3m.primitives.data_transformation.encoder.DistilTextEncoder'],

'REMOTESENSING': ['d3m.primitives.data_transformation.denormalize.Common',
                  'd3m.primitives.data_transformation.dataset_to_dataframe.Common',
                  'd3m.primitives.data_transformation.satellite_image_loader.DistilSatelliteImageLoader',
                  'd3m.primitives.data_transformation.column_parser.Common',
                  'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common', # images
                  'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
                  'd3m.primitives.remote_sensing.remote_sensing_pretrained.RemoteSensingPretrained'],

'AUDIO': ['d3m.primitives.data_transformation.audio_reader.DistilAudioDatasetLoader',
          'd3m.primitives.data_transformation.column_parser.Common',
          'd3m.primitives.data_transformation.extract_columns_by_semantic_types.Common',  # targets
          'd3m.primitives.feature_extraction.audio_transfer.DistilAudioTransfer']}

classifiers = [#'d3m.primitives.classification.multinomial_naive_bayes.SKlearn',
               'd3m.primitives.classification.linear_discriminant_analysis.SKlearn',
               'd3m.primitives.classification.quadratic_discriminant_analysis.SKlearn',
               'd3m.primitives.classification.logistic_regression.SKlearn',
               'd3m.primitives.classification.ada_boost.SKlearn',
               'd3m.primitives.classification.linear_svc.SKlearn',
               'd3m.primitives.classification.extra_trees.SKlearn',
               'd3m.primitives.classification.random_forest.SKlearn',
               'd3m.primitives.classification.bagging.SKlearn',
               'd3m.primitives.classification.svc.SKlearn',
               'd3m.primitives.classification.passive_aggressive.SKlearn',
               'd3m.primitives.classification.mlp.SKlearn',
               'd3m.primitives.classification.xgboost_gbtree.Common',
               'd3m.primitives.classification.gradient_boosting.SKlearn']

regressors = ['d3m.primitives.regression.ridge.SKlearn',
              'd3m.primitives.regression.lasso.SKlearn',
              'd3m.primitives.regression.elastic_net.SKlearn',
              'd3m.primitives.regression.lasso_cv.SKlearn',
              'd3m.primitives.regression.ada_boost.SKlearn',
              'd3m.primitives.regression.linear_svr.SKlearn',
              'd3m.primitives.regression.random_forest.SKlearn',
              'd3m.primitives.regression.extra_trees.SKlearn',
              'd3m.primitives.regression.xgboost_gbtree.Common',
              'd3m.primitives.regression.bagging.SKlearn',
              'd3m.primitives.regression.mlp.SKlearn',
              'd3m.primitives.regression.gradient_boosting.SKlearn']

regressors_rpi = ['d3m.primitives.regression.random_forest.SKlearn',
                  'd3m.primitives.regression.extra_trees.SKlearn',
                  'd3m.primitives.regression.gradient_boosting.SKlearn']

classifiers_rpi = ['d3m.primitives.classification.random_forest.SKlearn',
                   'd3m.primitives.classification.extra_trees.SKlearn',
                   'd3m.primitives.classification.gradient_boosting.SKlearn',
                   'd3m.primitives.classification.linear_discriminant_analysis.SKlearn']

sslVariants = ['d3m.primitives.classification.gradient_boosting.SKlearn',
               'd3m.primitives.classification.extra_trees.SKlearn',
               'd3m.primitives.classification.random_forest.SKlearn',
               'd3m.primitives.classification.bagging.SKlearn',
               'd3m.primitives.classification.linear_svc.SKlearn',
               'd3m.primitives.classification.svc.SKlearn']
