Auto\ :sup:`n`\  ML core functionalities
----

1. **Runs as server waiting to hear TA3 client GRPC requests on port 45042**

.. code:: shell

    ./src/main.py ta2ta3

2. **Runs in stand-alone TA2 mode without any client/TA2-3 API. This will search on TRAIN data for valid pipelines and output them**

.. code:: shell

    ./src/main.py search.

3. **For a given dataset-problem specification**
    - Search for valid pipelines (solutions)
    - Produce top pipelines with ranks. Pipelines are output as JSON files for evaluation purposes
    - Enable scoring, fit, produce on any pipeline. These calls are invoked from TA3

4. **TA2 pipelines can be evaluated independently using D3M’s reference runtime framework on the TRAIN-TEST dataset splits. 
(See scripts/run.sh)**



*“Pipeline” and “solution” are aliases and mean the same concept in TA2. A pipeline or solution is an end-to-end flowchart (DAG) composed of TA1 primitives, their hyperparameters and their connections to build model on the TRAIN data and produce predictions on the TEST data.*


