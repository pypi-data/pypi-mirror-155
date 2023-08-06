CMU TA2 (Built using DARPA D3M ecosystem)
=========================================

Auton ML is an automated machine learning system developed by CMU Auton
Lab to power data scientists with efficient model discovery and advanced
data analytics. Auton ML also powers the D3M Subject Matter Expert (SME)
User Interfaces such as Two Ravens http://2ra.vn/.

**Taking your machine learning capacity to the nth power.**

We provide a documentation listing the complete set of tasks, data
modalities, machine learning models and future supported tasks provided
by AutonML
`here <https://gitlab.com/sray/cmu-ta2/-/blob/dev/docs/SUPPORTED.md>`__.

Installation
------------

AutonML can be installed as: ``pip install autonml``. We recommend this
installation be done in a new virtual environment or conda environment.

Recommended steps to install ``autonml``:

.. code:: bash

   pip install autonml
   pip install d3m-common-primitives d3m-sklearn-wrap sri-d3m rpi-d3m-primitives dsbox-primitives dsbox-corex distil-primitives d3m-esrnn d3m-nbeats 
   pip install kf-d3m-primitives

This installation may take time to complete, owing to the fact that
pip's dependecy resolvers may take time resolving potential package
conflicts. To make installation faster, you can add pip's legacy
resolver as ``--use-deprecated=legacy-resolver``. Caution: using old
resolvers may present unresolved package conflicts.

D3M dataset
-----------

-  Any dataset to be used should be in D3M dataset format (directory
   structure with TRAIN, TEST folders and underlying .json files).
-  Example available of a single dataset
   `here <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/185_baseball_MIN_METADATA>`__
-  More datasets available
   `here <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/>`__
-  Any non-D3M data can be converted to D3M dataset. (See section below
   on “Convert raw dataset to D3M dataset”).

Run the AutonML pipeline
------------------------

We can run the AutonML pipeline in two ways.

**Command Line Interface** 

It can be run as a standalone CLI command,
accessed via the ``autonml_main`` command. This command takes five
arguments, listed below: 

-  Path to the data directory (must be in D3M format) 
-  Output directory where results are to be stored. This
directory will be dynamically created if it does not exist. 
-  Timeout (measured in minutes) 
-  Number of CPUs to be used (minimum: 4 cores, recommended: 8 cores) 
-  Path to ``problemDoc.json`` (see example below)

.. code:: bash

   INPUT_DIR=/home/<user>/d3m/datasets/185_baseball_MIN_METADATA
   OUTPUT_DIR=/output
   TIMEOUT=2
   NUMCPUS=8
   PROBLEMPATH=${INPUT_DIR}/TRAIN/problem_TRAIN/problemDoc.json

   autonml_main ${INPUT_DIR} ${OUTPUT_DIR} ${TIMEOUT} ${NUMCPUS} ${PROBLEMPATH} 

**API** 

AutonML can also be accessed via a simple Python API, as shown
in the command below.

.. code:: python

   from autonml import AutonML

   aml = AutonML(input_dir='/path/to/input/d3mdataset',
                 output_dir='/path/to/store/results',
                 timeout=10,
                 numpcpus=8)

   aml.run()

The above script will do the following- 

1.  Run search for best pipelines for the specified dataset using ``TRAIN`` data. 
2.  JSON pipelines (with ranks) will be output in JSON format at ``/output/pipelines_ranked/``.
3.  CSV prediction files of the pipelines trained on ``TRAIN`` data and
predicted on ``TEST`` data will be available at ``/output/predictions/`` 
4.  Training data predictions (cross-validated mostly) are produced in the current directory as ``/output/training_predictions/<pipeliname>_train_predictions.csv.`` 
5.  Python code equivalent of executing a JSON pipeline on a dataset produced at ``/output/executables/``

An example -

.. code:: bash

   OUTPUT_DIR=output

   python ${OUTPUT_DIR}/99211bc3-638a-455b-8d48-0dadc0bf1f10/executables/19908fd3-706a-48da-b13c-dc13da0ed3cc.code.py ${OUTPUT_DIR}/ ${OUTPUT_DIR}/99211bc3-638a-455b-8d48-0dadc0bf1f10/predictions/19908fd3-706a-48da-b13c-dc13da0ed3cc.predictions.csv

You can find example notebooks for various supported datasets
`here <https://gitlab.com/autonlab/d3m/autonml/-/tree/dev/examples>`__.

Convert raw dataset to D3M dataset
----------------------------------

.. _d3m-dataset-1:

D3M dataset
~~~~~~~~~~~

-  Any dataset to be used should be in D3M dataset format (directory
   structure with TRAIN, TEST folders and underlying .json files).
-  Example available of a single dataset
   `here <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/185_baseball_MIN_METADATA>`__
-  More datasets available
   `here <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/>`__
-  Any non-D3M data can be converted to D3M dataset. (See section below
   on “Convert raw dataset to D3M dataset”).

.. _convert-raw-dataset-to-d3m-dataset-1:

`API <https://gitlab.com/autonlab/d3m/autonml/-/blob/dev/docs/convert_d3m_data.rst>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If not done already, run ``pip install autonml`` before our raw dataset
converter.

.. code:: bash

   create_d3m_dataset <train_data.csv> <test_data.csv> <label> <metric> -t classification <-t ...>

Detailed description of dataset type(s), task type(s) and metrics
supported can be found `here <https://gitlab.com/autonlab/d3m/autonml/-/blob/dev/docs/convert_d3m_data.rst>`__\ **.**
