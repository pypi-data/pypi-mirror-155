Auto\ :sup:`n`\ ML code structure
----

All of the following files are built into Auto\ :sup:`n`\ ML docker image

1. **src/solution_templates.py:** 
    - Contains pipeline templates for different task types, data types and different models being evaluated
    - Pipeline templates for classification/regression are not complete. They require the model (classifier/regressor) to be appended followed by "construct_predictions" primitive step
    - Even for graph-based problems, like vertex nomination, graph matching etc., we add classification templates since they can work with the main table to produce good predictions

2. **src/auto_solutions.py:**
    - Creates the set of all valid pipelines for a dataset. These pipelines have not been scored/fitted as yet. However, common steps of pipelines have been already run in run_basic_solution() before we copy the basic solution for multiple models (classifiers/regressors)
    - Contains rules for pruning set of pipelines based on ML task type, dataset rows, columns etc

3. **src/solutiondescription.py:**
    - Contains class "SolutionDescription" for a single pipeline/solution
    - Contains methods to initialize, score, fit, produce, and describe a pipeline
    - *initialize_solution()* is important for constructing the complete pipeline from the respective template. This creates the entire pipeline end-to-end making the appropriate connections
    - *run_basic_solution()* is used to run common preprocessing/featurizing steps before we copy and spawn multiple processes for evaluating different models (classifiers/regressors). This results in huge savings in time usage when processing complex data types
    - *score_solution()* is used to evaluate pipeline by running k-fold CV on the classifier/regressor model in the pipeline. This corresponds to the second-last step in the pipelines (before *construct_predictions*)

4. **src/api_v3/core.py:**
    - Contains server startup and methods for TA2-TA3 API (GRPC calls). See `this link <https://gitlab.com/datadrivendiscovery/ta3ta2-api/>`_. All GRPC messages are a part of core.proto file. Core.proto, pipeline.proto, primitive.proto and value.proto files contain all the information about these message structures

5. **src/search.py:**
    -  Runs Auto\ :sup:`n`\ ML in stand-alone evaluation mode

6. **src/*pb2*.py:**
    - These are auto-generated files by the rebuild_grpc.sh script. These handle the GRPC communication for TA2-TA3 API

7. **src/main.py:**
    - Contains Auto\ :sup:`n`\ ML startup code

8. **src/util.py:**
    - Contains some utility functions

9. **src/default_hyperparams.py:**
    - Contains default hyperparameter settings for several TA1 primitives. These hyperparameters are not tuned

10. **src/primitivedescription.py:**
    - Contains code for evaluating models/primitives using k-fold cross-validation
