Convert raw dataset to D3M dataset
==================================

Currently d3m package needs Python 3.6 only.

.. code:: shell

    pip install d3m
    python create_d3m_dataset.py <train_data.csv> <test_data.csv> <label> <metric> -t classification <-t ...>

Example
~~~~~~~

Some examples of valid commands (for tabular data) are -

.. code:: shell

    python create_d3m_dataset.py train_data.csv test_data.csv Label accuracy -t classification
    python create_d3m_dataset.py train_data.csv test_data.csv Value meanSquaredError -t regression

-t option should be used to specify task types(s), data types(s). metrics.
This script will create a directory structure "raw" for your dataset in D3M format.
This dataset should be used as input to ./scripts/start_container.sh

This is the structure created for a generated D3M dataset::

   raw$ tree
   .
   ├── TEST
   │   ├── dataset_TEST
   │   │   ├── datasetDoc.json
   │   │   ├── metadata.json
   │   │   └── tables
   │   │       └── learningData.csv
   │   └── problem_TEST
   │       └── problemDoc.json
   └── TRAIN
       ├── dataset_TRAIN
       │   ├── datasetDoc.json
       │   ├── metadata.json
       │   └── tables
       │       └── learningData.csv
       └── problem_TRAIN
           └── problemDoc.json

   8 directories, 8 files


Example of creating D3M dataset for image regression
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    python create_d3m_dataset.py train.csv test.csv WRISTBREADTH meanSquaredError -t regression -t image
    Namespace(dataFileName='train.csv', metric='meanSquaredError', target='WRISTBREADTH', tasks=['regression', 'image'], testDataFileName='test.csv')
    Going to create TRAIN files!
    Going to create TEST files!
    Please enter directory name for TRAIN media files: train_images
    Please enter directory name for TEST media files: test_images
    Please enter column name for media files: image_file

Note: Some task/data type(s) may not be entirely automated (Eg., object detection, graph problems). 
TRAIN, TEST hierarchies will be made available. However, datasetDoc.json might need to be customized for linking resources/tables for the specific task.
For this purpose, example datasets are provided for reference purposes.

Valid task types(s)
~~~~~~~~~~~

linkPrediction, graphMatching, forecasting, classification, semiSupervised,
clustering, collaborativeFiltering, regression, objectDetection, vertexNomination, communityDetection,
vertexClassification

- See detailed D3M dataset creation for ``forecasting`` at `forecasting documentation <https://gitlab.com/sray/cmu-ta2/-/blob/master/forecasting.rst>`__

Valid data type(s)
~~~~~~~~~~~~~~~~~~
Valid data type(s) to specify are- audio, image, video, text, timeSeries

- See detailed D3M dataset creation with ``image`` at `image documentation <https://gitlab.com/sray/cmu-ta2/-/blob/master/image.rst>`__
- See detailed D3M dataset creation with ``video`` at `video documentation <https://gitlab.com/sray/cmu-ta2/-/blob/master/video.rst>`__


Valid metrics
~~~~~~~~~~~~~

classification/linkPrediction/graphMatching/vertexNomination/vertexClassification: accuracy, f1Macro, f1Micro, rocAuc, rocAucMacro, rocAucMicro
regression/forecasting/collaborativeFiltering: rSquared, meanSquaredError, meanSquaredError, meanAbsoluteError
communityDetection/clustering: normalizedMutualInformation


Sample D3M dataset(s) for task type(s), data types(s):

- ``classification``: `185_baseball_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/185_baseball_MIN_METADATA>`__
- ``regression``: `196_autoMpg_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/196_autoMpg_MIN_METADATA>`__
- ``forecasting``: `LL1_736_stock_market_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/LL1_736_stock_market_MIN_METADATA>`__
- ``audio``: `31_urbansound_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/31_urbansound_MIN_METADATA>`__
- ``video``: `LL1_VID_UCF11_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/LL1_VID_UCF11_MIN_METADATA>`__
- ``text``: `LL1_TXT_CLS_airline_opinion_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/LL1_TXT_CLS_airline_opinion_MIN_METADATA>`__
- ``timeseries``: `66_chlorineConcentration_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/66_chlorineConcentration_MIN_METADATA>`__
- ``image``: `22_handgeometry_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/22_handgeometry_MIN_METADATA>`__
- ``collaborativeFiltering``: `60_jester_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/60_jester_MIN_METADATA>`__
- ``communityDetection``: `6_70_com_amazon_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/6_70_com_amazon_MIN_METADATA>`__
- ``graphMatching``: `49_facebook_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/49_facebook_MIN_METADATA>`__
- ``linkPrediction``: `59_umls_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/59_umls_MIN_METADATA>`__
- ``vertexClassification``: `LL1_VTXC_1343_cora_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/LL1_VTXC_1343_cora_MIN_METADATA>`__ 
