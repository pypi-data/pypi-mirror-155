# Summary

## Currently Supported Data Modalities

- Tabular
- Time-Series
- Text
- Image
- Video

## Currently Supported Tasks 
- Classification
- Regression
- Time Series Forecasting
- Object Detection

## Currently Supported D3M Primitives
- d3m-common-primitives 
- d3m-sklearn-wrap 
- sri-d3m rpi-d3m-primitives 
- dsbox-primitives 
- dsbox-corex 
- distil-primitives 
- d3m-esrnn 
- d3m-nbeats

## Currently Supported Machine Learning Models

### Models
- All standard Sklearn models (upto sklearn version ==1.22.2)
- ARIMA (Time Series Forecasting)
- ESRNN (Time Series Forecasting)
- DeepAR LSTM (Time Series Forecasting)
- NBeats (Time Series Forecasting)
- Vector Autoregression (Time Series Forecasting)
- XGBoost 
- BERT Classifier (Text)
- Distil TF-IDF Text Classifier (Text)
- ResNeXt 101 Kinetics Video Featurizer

### Featurizers
- TF-IDF vectorizer (Text)
- Distil Primitives Text Encoder (Text)
- Distil Image Transfer for Image Featurization (Image)
- Resnet-50 Image Featurizer (Image)

Specific models used by AutonML for Classification and Regression:

### Classifiers
- Linear Discriminant Analysis (SKlearn)
- Quadtratic Discriminant Analysis (SKlearn)
- Logistic Regression (SKlearn)
- Adaboost (SKlearn)
- Linear SVC (SKlearn)
- Extra Trees (SKlearn)
- Random Forest (SKlearn)
- Bagging (SKlearn)
- SVC (SKlearn)
- Passive Aggressive (SKlearn)
- MLP (SKlearn)
- XGBoost gbtree
- Gradient Boosting (SKlearn)


### Regressors
- Ridge Linear Model (SKlearn)
- Lasso Linear Model (SKlearn)
- ElasticNet (SKlearn)
- LassoCV (SKlearn)
- Adaboost (SKlearn)
- Linear SVR (SKlearn)
- Random Forest (SKlearn)
- Extra Trees (SKlearn)
- XGBoost gbtree (SKlearn)
- Bagging Regressor (SKlearn)
- MLP (SKlearn)
- Gradient Boosting (SKlearn)


# Future Supported Tasks

## Machine Learning Models to be Added to AutonML for Future Use

### Models
- FastLVM K-Means Clustering

### Featurizers
- Distil Audio Tranfer to Extract VGGish Audio Features (Audio)
- YOLO Image Featurizer (Object Detection)
- RetinaNet Object Featurizer (Object Detection)


## Future Supported Tasks
- Semi-Supervised Classification 
- Object Detection
- Classification and Regression (Video and Audio)
- Clustering
- Link Prediction
- Community Detection


## Future D3M Primitives Migration
- autonbox 
- fastlvm
- kf-d3m-primitives
- fastai-prims
- dsbox-graphs
