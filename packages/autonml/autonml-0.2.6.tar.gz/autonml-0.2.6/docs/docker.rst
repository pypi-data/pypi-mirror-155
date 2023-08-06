Running AutonML as a Container
============

Docker
----

Docker image available at 

.. code:: shell

    registry.gitlab.com/sray/cmu-ta2:latest


D3M dataset
----

The Auto\ :sup:`n`\ ML can accept any type of D3M dataset. 
If there is no D3M dataset, this is how a raw dataset is converted to a D3M
First install the d3m package

.. code:: shell

    pip install d3m
    python create_d3m_dataset.py <train_data.csv> <test_data.csv> <label> <metric> -t classification <-t ...>

*Currently d3m package needs Python 3.6 only*

Detailed description of dataset type(s), task type(s) and metrics provided in the `Converting raw data to d3m datasets section <https://cmu-ta2.readthedocs.io/en/master/convert_d3m_data.html>`_

Starting script
----

- Requires docker on your OS.
- Update location of your dataset for target "input" to the docker run.
- Run the following script

.. code:: shell

    ./scripts/start_container.sh

The above script has 4 mount points for the docker

1. input: Path of the input dataset
2. output: Directory where all outputs will be stored
3. static: Location of all static files (Use static directory of this repository)
4. scripts: Location of this repository's scripts.

Search and predictions
----

The above script will do the following

1. Pull docker image and run search for best pipelines for the specified dataset using TRAIN data
2. JSON pipelines (with ranks) will be output in JSON format at /output/<search_dir>/pipelines_ranked/
3. CSV prediction files of the pipelines trained on TRAIN data and predicted on TEST data will be available at /output/<search_dir>/predictions/
4. Training data predictions (cross-validated mostly) are produced in the current directory as /output/<search_dir>/training_predictions/<pipeline_id>_train_predictions.csv.
5. Python code equivalent of executing a JSON pipeline on a dataset produced at /output/<search_dir>/executables/

This code can be run as 

.. code:: python

    python <generated_code.py> <path_to_dataset> <predictions_output_file>

An example

.. code:: python

    python /output/6b92f2f7-74d2-4e86-958d-4e62bbd89c51/executables/131542c6-ea71-4403-9c2d-d899e990e7bd.json.code.py 185_baseball predictions.csv

- If feature_importances and intermediate outputs are desired, call scripts/run_outputs.sh instead of scripts/run.sh from scripts/start_container.sh
Features importances and intermediate step outputs will be produced in /output/<search_dir>/pipeline_runs/

