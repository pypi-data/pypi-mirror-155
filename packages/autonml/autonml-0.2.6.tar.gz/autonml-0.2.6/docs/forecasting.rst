Convert raw dataset to D3M dataset (For forecasting)
===============================================================================

Input requirements-
~~~~~~~~~~~~~~~~~~~

The following inputs are needed to be provided by the user on the command-line:

- ``training data file``: CSV file, eg. train.csv::

   $ cat train.csv 
   Company,Date,Close
   abbv,1/4/2013,28.81
   abbv,1/7/2013,28.869
   abbv,1/8/2013,28.241999999999997
   abbv,1/9/2013,28.399
   abbv,1/10/2013,28.480999999999998
   abbv,1/11/2013,28.695
   abbv,1/14/2013,28.899
   abbv,1/15/2013,29.331999999999997
   abbv,1/16/2013,30.127

- ``testing data file``: CSV file, eg. test.csv::

   $ cat test.csv 
   Company,Date,Close
   abbv,10/2/2017,89.764
   abbv,10/3/2017,89.079
   abbv,10/4/2017,89.277
   abbv,10/5/2017,89.555
   abbv,10/6/2017,89.863
   abbv,10/9/2017,90.15100000000001
   abbv,10/10/2017,90.538
   abbv,10/11/2017,91.74
   abbv,10/12/2017,91.42

- ``date/time column name``: Column name for the date/time attribute in train and test files. Accepted formats are ``10/2/2017`` (date format), ``330`` (sequence), ``1998`` (year)
- ``grouping column name``: Column name for the grouping attribute/category in train and test files

Example of creating D3M dataset for time series forecasting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We show two examples here for usage via the CLI interface and a pythonic interface.

.. code:: shell

    python create_d3m_dataset.py train.csv test.csv Close meanAbsoluteError -t forecasting
    Namespace(dataFileName='train.csv', metric='meanAbsoluteError', target='Close', tasks=['forecasting'], testDataFileName='test.csv')
    Going to create TRAIN files!
    __main__: Calling a deprecated function 'fix_uri' in 'create_d3m_dataset.py' at line 176: use path_to_uri instead
    Going to create TEST files!
    Please enter column name for date/time column: Date
    Please enter column name for grouping/category column: Company

.. code:: python

   from autonml import createD3MDataset 

    training_data_csv = 'train.csv'
    testing_data_csv = 'test.csv
    output_dir = 'path/to/formatted/data/output/directory'
    label = 'label'
    metric = 'meanAbsoluteError'
    tasks = ['forecasting']

    createD3MDataset(training_data_csv,
                     testing_data_csv,
                     output_dir,
                     label,
                     metric, 
                     tasks)

This is the datasetDoc.json created for the generated D3M dataset::

   "resType": "table",
   "columnsCount": 4,
   "resPath": "tables/learningData.csv",
   "columns": [
       {   
           "colIndex": 0,
           "colName": "d3mIndex",
           "role": [
               "index"
           ],
           "colType": "integer"
       },
       {   
           "colIndex": 1,
           "colName": "Company",
           "role": [
               "suggestedGroupingKey",
               "attribute"
           ],
           "colType": "categorical"
       },
       {   
           "colIndex": 2,
           "colName": "Date",
           "role": [
               "timeIndicator",
               "attribute"
           ],
           "colType": "dateTime"
       },
       {   
           "colIndex": 3,
           "colName": "Close",
           "role": [],
           "colType": "unknown"
       }
   ]

There can be multiple ``suggestedGroupingKey`` attributes or even none. Please modify accordingly in the datasetDoc.json file.

Example of D3M seed datasets for time series forecasting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `LL1_736_stock_market_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/LL1_736_stock_market_MIN_METADATA>`__ Here ``Company`` is the grouping attribute, ``Date`` is the date/time column and ``Close`` is the target::

   d3mIndex,Company,Date,Close
   0,abbv,1/4/2013,28.81
   1,abbv,1/7/2013,28.869
   2,abbv,1/8/2013,28.241999999999997
   3,abbv,1/9/2013,28.399
   4,abbv,1/10/2013,28.480999999999998
   5,abbv,1/11/2013,28.695
   6,abbv,1/14/2013,28.899
   7,abbv,1/15/2013,29.331999999999997
   8,abbv,1/16/2013,30.127

- `LL1_736_population_spawn_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/LL1_736_population_spawn_MIN_METADATA>`__ Here ``species`` and ``sector`` are the grouping attributes, ``day`` is the date/time column and ``count`` is the target::

   d3mIndex,species,sector,day,count
   0,cas9_VBBA,S_3102,4,28810
   1,cas9_VBBA,S_3102,7,28869
   2,cas9_VBBA,S_3102,8,28241
   3,cas9_VBBA,S_3102,9,28399
   4,cas9_VBBA,S_3102,10,28480
   5,cas9_VBBA,S_3102,11,28695
   6,cas9_VBBA,S_3102,14,28899
   7,cas9_VBBA,S_3102,15,29331
   8,cas9_VBBA,S_3102,16,30127
   
- `56_sunspots_MIN_METADATA <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/56_sunspots_MIN_METADATA>`__ Here there is no grouping attributes, ``year`` is the date/time column and ``sunspots`` is the target::

   d3mIndex,year,sd,observations,sunspots
   0,1818,9.2,213.0,52.9
   1,1819,7.9,249.0,38.5
   2,1820,6.4,224.0,24.2
   3,1821,4.2,304.0,9.2
   4,1822,3.7,353.0,6.3
   5,1823,2.7,302.0,2.2
   6,1824,4.6,194.0,11.4
   7,1825,6.8,310.0,28.2
   8,1826,9.8,320.0,59.9
