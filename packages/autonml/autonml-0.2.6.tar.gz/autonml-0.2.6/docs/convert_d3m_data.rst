Convert raw dataset to D3M dataset
==================================

The raw dataset converter requires python version >=3.6. It requires the core :code:`d3m` package 
be installed. It currently supports the following data types:

*  Text
*  Video
*  Image
*  Time-Series
*  Tabular

Note: Some task/data type(s) may not be entirely automated (Eg., object detection, graph problems). 
TRAIN, TEST hierarchies specific to D3M datasets will be made available. However, datasetDoc.json might 
need to be customized for linking resources/tables for the specific task. For this purpose, 
example datasets are provided for reference purposes.

Interface
^^^^^^^^^

Command Line
~~~~~~~~~~~~

.. code:: shell

    create_d3m_dataset <train_data.csv> <test_data.csv> <output_dir> <label> <metric> -t classification <-t ...>

API
^^^

.. code:: python

    from autonml import createD3MDataset 

    training_data_csv = 'path/to/train/data'
    testing_data_csv = 'path/to/test/data'
    output_dir = 'path/to/formatted/data/output/directory'
    label = 'Target'
    metric = 'f1Macro'
    tasks = ['classification']

    createD3MDataset(training_data_csv,
                     testing_data_csv,
                     output_dir,
                     label,
                     metric, 
                     tasks)

Usage and Explanation
~~~~~~~~~~~~~~~~~~~~~

Both the CLI command and the :code:`createD3MDataset` API require 6 mandatory arguments irrespective of the 
task type. In order, these arguments are:

*  **Input Training Data** : Path to input training datafile/directory. Please see the *Supported Formats for Input Datasets* subsection below
*  **Input Testing Data** : Path to input testing datafile/directory. Please see the *Supported Formats for Input Datasets* subsection below 
*  **Output directory** : Path to output directory for storing the converted D3M dataset. Creates the directory if it does not exist, but the parent directory must exist.
*  **Label** : Column name which points to the targets. This must be consistent between training and testing data.
*  **Metric** : Metric for evaluation. 
*  **Tasks** : A list of tags that define the task type for AutonML. Please refer to the *Valid task types* subsection. 


Detailed documentation on different data types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*  See detailed D3M dataset creation with ``image`` at `image documentation <https://gitlab.com/autonlab/d3m/autonml/-/blob/dev/docs/image.rst>`__
*  See detailed D3M dataset creation with ``video`` at `video documentation <https://gitlab.com/autonlab/d3m/autonml/-/blob/dev/docs/video.rst>`__
*  See detailed D3M dataset creation with ``forecasting`` at `forecasting documentation <https://gitlab.com/autonlab/d3m/autonml/-/blob/dev/docs/forecasting.rst>`__

Creation of ``text`` D3M datasets follows a similar methodology to creation of image datasets, 
please refer to the documentation on image datasets above for a similar archetype to text datasets.


Example
~~~~~~~

Some examples of valid commands are -

.. code:: shell

    create_d3m_dataset train_data.csv test_data.csv output_dir Label accuracy -t classification
    create_d3m_dataset train_data.csv test_data.csv output_dir Value meanSquaredError -t regression

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



Valid task type(s)
^^^^^^^^^^^^^^^^^^

linkPrediction, graphMatching, forecasting, classification, semiSupervised,
clustering, collaborativeFiltering, regression, objectDetection, vertexNomination, communityDetection,
vertexClassification

Valid metric(s)
^^^^^^^^^^^^^^^

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
