Convert raw dataset with images to D3M dataset (For classification/regression)
===============================================================================

Input requirements-
~~~~~~~~~~~~~~~~~~~

The following inputs are needed to be provided by the user on the command-line:

- ``training data file``: CSV file, eg. train.csv with image file column(first) and target (label)::

   $ cat train.csv 
   image_file,label
   bdcdb0246dfe297cd3f9b1d3450ebb130bb321c0.jpg,stenosis
   37d6946b44f2230ca444f9dcb8d6d9790c4f18eb.jpg,stenosis
   cf0eac4f0f32979588f560f5edaf8fcef45a18d7.jpg,stenosis
   256d4f3f460536916a2b475cf273ac0aa026932c.jpg,stenosis
   d204c3a85cbf41c4663f53d2cf0f6c7385b61315.jpg,stenosis
   21ec3234d71bec1011c73ad73d47d4d1716edab1.jpg,no_stenosis
   bfccd11f7bd615f8602516d00443cb4160f35a0c.jpg,stenosis
   d4f5c15758f596c0ceb4a6b32d5aff629131f9b5.jpg,stenosis
   cbf2be2736586357e545988039f2223782dc4e0c.jpg,no_stenosis

- ``testing data file``: CSV file, eg. test.csv with input file column(first) and target (label)::

   $ cat test.csv 
   image_file,label
   5c02056848954352f7361952ecb4408538ffb002.jpg,stenosis
   58d544f8e0ba6502c08f54889274598ce9da936d.jpg,stenosis
   95f8006ed741fc73684895410d23ac030b8f2c14.jpg,no_stenosis
   31b9aace44946223806964540bd22fa1991028d5.jpg,no_stenosis
   ca651681b6bf44f572fc9a16ef62bb4cc0bf61cd.jpg,stenosis
   7f8b660a340eaec34884846ea8b2b0127102b5f1.jpg,stenosis
   0dc2e1d41fb7e0ff857490d0ddaaaa30e4002c20.jpg,stenosis
   887403d8353b1dc31ee1a342a838b2b7afbeb52e.jpg,stenosis
   02e0d1947e4a2c6438ede4ae2902fcab81898939.jpg,no_stenosis

- ``train_images``: Directory containing images referenced by training data file::

   $ ls train_images/
   21ec3234d71bec1011c73ad73d47d4d1716edab1.jpg  bdcdb0246dfe297cd3f9b1d3450ebb130bb321c0.jpg  cf0eac4f0f32979588f560f5edaf8fcef45a18d7.jpg
   256d4f3f460536916a2b475cf273ac0aa026932c.jpg  bfccd11f7bd615f8602516d00443cb4160f35a0c.jpg  d204c3a85cbf41c4663f53d2cf0f6c7385b61315.jpg
   37d6946b44f2230ca444f9dcb8d6d9790c4f18eb.jpg  cbf2be2736586357e545988039f2223782dc4e0c.jpg  d4f5c15758f596c0ceb4a6b32d5aff629131f9b5.jpg

- ``test_images``: Directory containing images referenced by testing data file::

   $ ls test_images/
   02e0d1947e4a2c6438ede4ae2902fcab81898939.jpg  58d544f8e0ba6502c08f54889274598ce9da936d.jpg  887403d8353b1dc31ee1a342a838b2b7afbeb52e.jpg
   0dc2e1d41fb7e0ff857490d0ddaaaa30e4002c20.jpg  5c02056848954352f7361952ecb4408538ffb002.jpg  95f8006ed741fc73684895410d23ac030b8f2c14.jpg
   31b9aace44946223806964540bd22fa1991028d5.jpg  7f8b660a340eaec34884846ea8b2b0127102b5f1.jpg  ca651681b6bf44f572fc9a16ef62bb4cc0bf61cd.jpg


Example of creating D3M dataset for image classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We show two examples here for usage via the CLI interface and a pythonic interface.

.. code:: shell

    python create_d3m_dataset.py train.csv test.csv label accuracy -t classification -t image

    # Output
    Namespace(dataFileName='train.csv', metric='accuracy', target='label', tasks=['classification', 'image'], testDataFileName='test.csv')
    Going to create TRAIN files!
    Going to create TEST files!
    Please enter directory name for TRAIN media files: train_images
    Please enter directory name for TEST media files: test_images
    Please enter column name for media files: image_file

.. code:: python

   from autonml import createD3MDataset 

    training_data_csv = 'train.csv'
    testing_data_csv = 'test.csv
    output_dir = 'path/to/formatted/data/output/directory'
    label = 'label'
    metric = 'f1Macro'
    tasks = ['classification', 'image']

    createD3MDataset(training_data_csv,
                     testing_data_csv,
                     output_dir,
                     label,
                     metric, 
                     tasks)

   


This is the structure created for the generated D3M dataset::

   raw$ tree
   .
   ├── TEST
   │   ├── dataset_TEST
   │   │   ├── datasetDoc.json
   │   │   ├── media
   │   │   │   ├── 02e0d1947e4a2c6438ede4ae2902fcab81898939.jpg
   │   │   │   ├── 0dc2e1d41fb7e0ff857490d0ddaaaa30e4002c20.jpg
   │   │   │   ├── 31b9aace44946223806964540bd22fa1991028d5.jpg
   │   │   │   ├── 58d544f8e0ba6502c08f54889274598ce9da936d.jpg
   │   │   │   ├── 5c02056848954352f7361952ecb4408538ffb002.jpg
   │   │   │   ├── 7f8b660a340eaec34884846ea8b2b0127102b5f1.jpg
   │   │   │   ├── 887403d8353b1dc31ee1a342a838b2b7afbeb52e.jpg
   │   │   │   ├── 95f8006ed741fc73684895410d23ac030b8f2c14.jpg
   │   │   │   └── ca651681b6bf44f572fc9a16ef62bb4cc0bf61cd.jpg
   │   │   ├── metadata.json
   │   │   └── tables
   │   │       └── learningData.csv
   │   └── problem_TEST
   │       └── problemDoc.json
   └── TRAIN
       ├── dataset_TRAIN
       │   ├── datasetDoc.json
       │   ├── media
       │   │   ├── 21ec3234d71bec1011c73ad73d47d4d1716edab1.jpg
       │   │   ├── 256d4f3f460536916a2b475cf273ac0aa026932c.jpg
       │   │   ├── 37d6946b44f2230ca444f9dcb8d6d9790c4f18eb.jpg
       │   │   ├── bdcdb0246dfe297cd3f9b1d3450ebb130bb321c0.jpg
       │   │   ├── bfccd11f7bd615f8602516d00443cb4160f35a0c.jpg
       │   │   ├── cbf2be2736586357e545988039f2223782dc4e0c.jpg
       │   │   ├── cf0eac4f0f32979588f560f5edaf8fcef45a18d7.jpg
       │   │   ├── d204c3a85cbf41c4663f53d2cf0f6c7385b61315.jpg
       │   │   └── d4f5c15758f596c0ceb4a6b32d5aff629131f9b5.jpg
       │   ├── metadata.json
       │   └── tables
       │       └── learningData.csv
       └── problem_TRAIN
           └── problemDoc.json

   10 directories, 26 files

Default file format for images is ``jpg``.
If using a different file format, for eg., ``png``, replace the following in ``raw/TRAIN/dataset_TRAIN/datasetDoc.json``::

   "resFormat": {
       "image/jpeg": [
           "jpeg",
           "jpg"
       ]
   },

to::

   "resFormat": {
       "image/png": [
           "png"
       ]
   },


Example of D3M seed dataset for image regression
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``image``: `22_handgeometry <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/22_handgeometry_MIN_METADATA>`__

Example of D3M seed dataset for image (with .png file formats) classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``image``: `124_214_coil20 <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/124_214_coil20_MIN_METADATA>`__
