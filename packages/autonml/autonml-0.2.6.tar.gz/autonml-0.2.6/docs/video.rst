Convert raw dataset with videos to D3M dataset (For classification/regression)
===============================================================================

Input requirements-
~~~~~~~~~~~~~~~~~~~

The following inputs are needed to be provided by the user on the command-line:

- ``training data file``: CSV file, eg. train.csv with video file column(first) and target (label)::

   $ cat train.csv 
   video_file,label
   bdcdb0246dfe297cd3f9b1d3450ebb130bb321c0.mp4,stenosis
   37d6946b44f2230ca444f9dcb8d6d9790c4f18eb.mp4,stenosis
   cf0eac4f0f32979588f560f5edaf8fcef45a18d7.mp4,stenosis
   256d4f3f460536916a2b475cf273ac0aa026932c.mp4,stenosis
   d204c3a85cbf41c4663f53d2cf0f6c7385b61315.mp4,stenosis
   21ec3234d71bec1011c73ad73d47d4d1716edab1.mp4,no_stenosis
   bfccd11f7bd615f8602516d00443cb4160f35a0c.mp4,stenosis
   d4f5c15758f596c0ceb4a6b32d5aff629131f9b5.mp4,stenosis
   cbf2be2736586357e545988039f2223782dc4e0c.mp4,no_stenosis

- ``testing data file``: CSV file, eg. test.csv with input file column(first) and target (label)::

   $ cat test.csv 
   video_file,label
   5c02056848954352f7361952ecb4408538ffb002.mp4,stenosis
   58d544f8e0ba6502c08f54889274598ce9da936d.mp4,stenosis
   95f8006ed741fc73684895410d23ac030b8f2c14.mp4,no_stenosis
   31b9aace44946223806964540bd22fa1991028d5.mp4,no_stenosis
   ca651681b6bf44f572fc9a16ef62bb4cc0bf61cd.mp4,stenosis
   7f8b660a340eaec34884846ea8b2b0127102b5f1.mp4,stenosis
   0dc2e1d41fb7e0ff857490d0ddaaaa30e4002c20.mp4,stenosis
   887403d8353b1dc31ee1a342a838b2b7afbeb52e.mp4,stenosis
   02e0d1947e4a2c6438ede4ae2902fcab81898939.mp4,no_stenosis

- ``train_videos``: Directory containing videos referenced by training data file::

   $ ls train_videos/
   21ec3234d71bec1011c73ad73d47d4d1716edab1.mp4  bdcdb0246dfe297cd3f9b1d3450ebb130bb321c0.mp4  cf0eac4f0f32979588f560f5edaf8fcef45a18d7.mp4
   256d4f3f460536916a2b475cf273ac0aa026932c.mp4  bfccd11f7bd615f8602516d00443cb4160f35a0c.mp4  d204c3a85cbf41c4663f53d2cf0f6c7385b61315.mp4
   37d6946b44f2230ca444f9dcb8d6d9790c4f18eb.mp4  cbf2be2736586357e545988039f2223782dc4e0c.mp4  d4f5c15758f596c0ceb4a6b32d5aff629131f9b5.mp4

- ``test_videos``: Directory containing videos referenced by testing data file::

   $ ls test_videos/
   02e0d1947e4a2c6438ede4ae2902fcab81898939.mp4  58d544f8e0ba6502c08f54889274598ce9da936d.mp4  887403d8353b1dc31ee1a342a838b2b7afbeb52e.mp4
   0dc2e1d41fb7e0ff857490d0ddaaaa30e4002c20.mp4  5c02056848954352f7361952ecb4408538ffb002.mp4  95f8006ed741fc73684895410d23ac030b8f2c14.mp4
   31b9aace44946223806964540bd22fa1991028d5.mp4  7f8b660a340eaec34884846ea8b2b0127102b5f1.mp4  ca651681b6bf44f572fc9a16ef62bb4cc0bf61cd.mp4


Example of creating D3M dataset for video classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We show two examples here for usage via the CLI interface and a pythonic interface.

.. code:: shell

    python create_d3m_dataset.py train.csv test.csv label accuracy -t classification -t video
    Namespace(dataFileName='train.csv', metric='accuracy', target='label', tasks=['classification', 'video'], testDataFileName='test.csv')
    Going to create TRAIN files!
    Going to create TEST files!
    Please enter directory name for TRAIN media files: train_videos
    Please enter directory name for TEST media files: test_videos
    Please enter column name for media files: video_file

.. code:: python

   from autonml import createD3MDataset 

    training_data_csv = 'train.csv'
    testing_data_csv = 'test.csv
    output_dir = 'path/to/formatted/data/output/directory'
    label = 'label'
    metric = 'accuracy'
    tasks = ['classification', 'video']

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
   │   │   │   ├── 02e0d1947e4a2c6438ede4ae2902fcab81898939.mp4
   │   │   │   ├── 0dc2e1d41fb7e0ff857490d0ddaaaa30e4002c20.mp4
   │   │   │   ├── 31b9aace44946223806964540bd22fa1991028d5.mp4
   │   │   │   ├── 58d544f8e0ba6502c08f54889274598ce9da936d.mp4
   │   │   │   ├── 5c02056848954352f7361952ecb4408538ffb002.mp4
   │   │   │   ├── 7f8b660a340eaec34884846ea8b2b0127102b5f1.mp4
   │   │   │   ├── 887403d8353b1dc31ee1a342a838b2b7afbeb52e.mp4
   │   │   │   ├── 95f8006ed741fc73684895410d23ac030b8f2c14.mp4
   │   │   │   └── ca651681b6bf44f572fc9a16ef62bb4cc0bf61cd.mp4
   │   │   ├── metadata.json
   │   │   └── tables
   │   │       └── learningData.csv
   │   └── problem_TEST
   │       └── problemDoc.json
   └── TRAIN
       ├── dataset_TRAIN
       │   ├── datasetDoc.json
       │   ├── media
       │   │   ├── 21ec3234d71bec1011c73ad73d47d4d1716edab1.mp4
       │   │   ├── 256d4f3f460536916a2b475cf273ac0aa026932c.mp4
       │   │   ├── 37d6946b44f2230ca444f9dcb8d6d9790c4f18eb.mp4
       │   │   ├── bdcdb0246dfe297cd3f9b1d3450ebb130bb321c0.mp4
       │   │   ├── bfccd11f7bd615f8602516d00443cb4160f35a0c.mp4
       │   │   ├── cbf2be2736586357e545988039f2223782dc4e0c.mp4
       │   │   ├── cf0eac4f0f32979588f560f5edaf8fcef45a18d7.mp4
       │   │   ├── d204c3a85cbf41c4663f53d2cf0f6c7385b61315.mp4
       │   │   └── d4f5c15758f596c0ceb4a6b32d5aff629131f9b5.mp4
       │   ├── metadata.json
       │   └── tables
       │       └── learningData.csv
       └── problem_TRAIN
           └── problemDoc.json

   10 directories, 26 files

Default file format for videos is ``.mp4``.
If using a different file format, replace the format(s) in ``raw/TRAIN/dataset_TRAIN/datasetDoc.json``::

   "resFormat": {
       "video/mp4": [
           "mp4"
       ]
   },


Example of D3M seed dataset for video classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``video``: `LL1_3476_HMDB_actio_recognition <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/LL1_3476_HMDB_actio_recognition_MIN_METADATA>`__
- ``video``: `LL1_VID_UCF11 <https://datasets.datadrivendiscovery.org/d3m/datasets/-/tree/master/seed_datasets_current/LL1_VID_UCF11_actio_recognition_MIN_METADATA>`__
