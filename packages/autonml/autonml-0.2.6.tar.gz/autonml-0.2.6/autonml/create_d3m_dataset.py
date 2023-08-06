 
#!/usr/bin/env python3

# File: create_d3m_dataset.py 
# Author(s): Saswati Ray
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

from genericpath import isdir
import json
import argparse
from multiprocessing.sharedctypes import Value
import shutil
import os, logging
from os.path import exists
from datetime import datetime
import pandas as pd

# d3m imports
from d3m.container import Dataset
from d3m.utils import fix_uri
from d3m.container.utils import save_container

basic_json_problem = {
  "about": {
    "problemID": "raw_problem",
    "problemName": "raw_problem",
    "problemVersion": "1.0",
    "problemSchemaVersion": "4.1.0",
    "taskKeywords": [
      "classification"
    ]
  },
  "inputs": {
    "data": [
      {
        "datasetID": "raw_dataset",
        "targets": [
          {
            "targetIndex": 0,
            "resID": "learningData",
            "colIndex": 18,
            "colName": "LABEL"
          }
        ]
      }
    ],
    "performanceMetrics": [
      {
        "metric": "f1Macro"
      }
    ]
  },
  "expectedOutputs": {
    "predictionsFile": "predictions.csv"
  }
}

TF_TRAINDIR = None
TF_TESTDIR = None
TF_COLNAME = None

# Pretty print JSON for debugging
def _pretty_print(json_dict):
    print(json.dumps(json_dict, indent=4, default=str))

# Copy media files as symlinks
def copySymDir(src, dst, tf_format=False):
    # Create destination directory if it does not already exist
    if not os.path.exists(dst):
        os.mkdir(dst)

    if not tf_format:    
        for filename in os.listdir(src):
            os.symlink(os.path.join(src, filename), os.path.join(dst, filename))
    else:
        for labeldir in os.listdir(src):
            for filename in os.listdir(os.path.join(src, labeldir)):
                filepath = os.path.join(src, labeldir, filename)
                if not os.path.isdir(filepath):
                    os.symlink(filepath, os.path.join(dst, f'{labeldir}_'+filename))

# Checks input datetime for a variety of different datetime formats
def validate_datetime(date_text):
    correct_flag = False
    
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        correct_flag = False

    try:
        datetime.strptime(date_text, '%d-%m-%Y')
        return True
    except ValueError:
        correct_flag = False

    try:
        datetime.strptime(date_text, '%m-%d-%Y')
        return True
    except ValueError:
        correct_flag = False
    
    try:
        datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        correct_flag = False

    try:
        datetime.strptime(date_text, '%d-%m-%Y %H:%M:%S')
        return True
    except ValueError:
        correct_flag = False

    try:
        datetime.strptime(date_text, '%m-%d-%Y %H.%M.%S')
        return True
    except ValueError:
        correct_flag = False

    try:
        datetime.strptime(date_text, '%Y-%m-%d %H.%M.%S')
        return True
    except ValueError:
        correct_flag = False

    try:
        datetime.strptime(date_text, '%d-%m-%Y %H.%M.%S')
        return True
    except ValueError:
        correct_flag = False

    try:
        datetime.strptime(date_text, '%m-%d-%Y %H.%M.%S')
        return True
    except ValueError:
        correct_flag = False

    # If none of the datetime formats have been matched
    return False

# Validate time column
#def validate_timecolumns()

# Get file formats for image/audio/video
def getFormat(t):
    if t == "image":
        return {"image/jpeg": ["jpeg", "jpg"]}
    elif t == "text":
        return {"text/plain": ["txt"]}
    elif t == "audio":
        return {
        "audio/wav": [
          "wav"
        ],
        "audio/aiff": [
          "aif",
          "aiff"
        ],
        "audio/flac": [
          "flac"
        ],
        "audio/ogg": [
          "ogg"
        ],
        "audio/mpeg": [
          "mp3"
        ]
      }
    else:
        return {
        "video/mp4": [
          "mp4"
        ]
      }

# Process task time series forecasting
def process_forecasting_task(TRAIN_DATASET_PATH, TEST_DATASET_PATH):
    # TODO : add error processing here 
    print("Enter time columns(s) and grouping column(s) at the prompts below. Grouping column may not be required for this dataset and the grouping prompt may be left empty. If multiple entries need to be entered for the prompts, please make sure they're separated by a space.")

    time_column = input("Please enter column name(s) for date/time column: ")
    grouping_column = input("Please enter column name(s) for grouping/category column: ")

    # TODO : add error checking here for incorrect prompts entered
    # Converting prompts to a set instead of lists ensures duplicate entries are handled
    time_column = set(time_column.split(' '))
    grouping_column = set(grouping_column.split(' '))

    for PATH in [TRAIN_DATASET_PATH, TEST_DATASET_PATH]:
        with open(PATH+'datasetDoc.json') as f:
            basic_json_dataset = json.load(f)
            #print(basic_json_dataset)
            columns = basic_json_dataset["dataResources"][0]["columns"]
            for c in columns:
                if c["colName"] in time_column:
                    c["role"].append("timeIndicator")
                    c["role"].append("attribute")
                    c["colType"] = "dateTime"
                elif c["colName"] in grouping_column:
                    c["role"].append("suggestedGroupingKey")
                    c["role"].append("attribute")
                    c["colType"] = "categorical"

        with open(PATH+'datasetDoc.json', "w") as jsonFile:
            json.dump(basic_json_dataset, jsonFile, indent=4)    

# Process task keywords for image, audio, video, text, timeSeries
def process_tasks(tasks, TRAIN_DATASET_PATH, TEST_DATASET_PATH, tf_format):
    for t in tasks:
        # Multimedia datasets
        if t == "image" or t == "audio" or t == "video" or t == "text":
            if not tf_format:
                trainMediaDir = input("Please enter directory name for TRAIN media files: ")  
                testMediaDir = input("Please enter directory name for TEST media files: ")
                image_column = input("Please enter column name for media files: ")
            else:
                trainMediaDir = TF_TRAINDIR
                testMediaDir = TF_TESTDIR
                image_column = TF_COLNAME

            media = {}
            media["resID"] = "0"
            media["resPath"] = "media/"
            media["resType"] = t
            media["resFormat"] = getFormat(t)
            media["isCollection"] = True

            for PATH in [TRAIN_DATASET_PATH, TEST_DATASET_PATH]: 
                with open(PATH+'datasetDoc.json') as f:
                    basic_json_dataset = json.load(f)
                columns = basic_json_dataset["dataResources"][0]["columns"]
                for c in columns:
                    if c["colName"] == image_column:
                        c["role"].append("attribute")
                        c["colType"] = "string"
                        c["refersTo"] = {"resID": "0", "resObject": "item"}
                basic_json_dataset["dataResources"].append(media)
                with open(PATH+'datasetDoc.json', "w") as jsonFile:
                    json.dump(basic_json_dataset, jsonFile, indent=4)

            copySymDir(trainMediaDir, TRAIN_DATASET_PATH+'media', tf_format)
            copySymDir(testMediaDir, TEST_DATASET_PATH+'media', tf_format)
        elif t == "timeSeries":
            trainTSDir = input("Please enter directory name for TRAIN TimeSeries files: ")
            testTSDir = input("Please enter directory name for TEST TimeSeries files: ")
            timeseries_column = input("Please enter column name for timeseries files: ")
            media = {}
            media["resID"] = "0"
            media["resPath"] = "timeseries/"
            media["resType"] = "timeseries"
            media["resFormat"] = {"text/csv": ["csv"]}
            media["isCollection"] = True
            media["columns"] = []
            media["columns"].append({"colIndex": 0, "colName": "time", "colType": "integer", "role": ["timeIndicator"]})

            for PATH in [TRAIN_DATASET_PATH, TEST_DATASET_PATH]:
                with open(PATH+'datasetDoc.json') as f:
                    basic_json_dataset = json.load(f)
                columns = basic_json_dataset["dataResources"][0]["columns"]
                for c in columns:
                    if c["colName"] == timeseries_column:
                        c["role"].append("attribute")
                        c["colType"] = "string"
                        c["refersTo"] = {"resID": "0", "resObject": "item"}
                basic_json_dataset["dataResources"].insert(0, media)
                with open(PATH+'datasetDoc.json', "w") as jsonFile:
                    json.dump(basic_json_dataset, jsonFile, indent=4)
            copySymDir(trainTSDir, TRAIN_DATASET_PATH+'timeseries')
            copySymDir(testTSDir, TEST_DATASET_PATH+'timeseries')
        elif t == "forecasting":
            process_forecasting_task(TRAIN_DATASET_PATH, TEST_DATASET_PATH)


# Create TRAIN and TEST directories. Creates d3mIndex column for each data file.
def create_directories(DATASET_PATH, PROBLEM_PATH, dataFileName, target_name, basic_json_problem):
    if exists(DATASET_PATH):
        shutil.rmtree(DATASET_PATH)
    if exists(PROBLEM_PATH):
        shutil.rmtree(PROBLEM_PATH)

    dataset = Dataset.load(fix_uri(dataFileName), dataset_id='raw_dataset')
    save_container(dataset, DATASET_PATH)

    colIndex = dataset['learningData'].columns.get_loc(target_name)
    basic_json_problem["inputs"]["data"][0]['targets'][0]['colIndex'] = colIndex
    
    os.makedirs(PROBLEM_PATH)
    with open(PROBLEM_PATH+"/problemDoc.json", "w") as jsonFile:
        json.dump(basic_json_problem, jsonFile, indent=4)
    with open(DATASET_PATH+'datasetDoc.json') as f:
        basic_json_dataset = json.load(f)
    basic_json_dataset["about"]["datasetSchemaVersion"] = "4.1.0"
    basic_json_dataset["about"]["datasetVersion"] = "1.0" 
    with open(DATASET_PATH+'datasetDoc.json', "w") as jsonFile:
        json.dump(basic_json_dataset, jsonFile, indent=4)

# Convert tensorflow formatted directories to TRAIN and TEST CSVs
def create_dataFiles(dataDir, dataOutputDir, type='train'):
    global TF_COLNAME
    TF_COLNAME = 'filename'
    data_dict = {'filename':[], 'label':[]}

    for labeldirs in os.listdir(dataDir):
        for filename in os.listdir(os.path.join(dataDir, labeldirs)):
            if not os.path.isdir(os.path.join(dataDir, labeldirs, filename)):
                data_dict['filename'].append(f'{labeldirs}_'+filename)
                data_dict['label'].append(labeldirs)

    data_df = pd.DataFrame.from_dict(data_dict)
    dataFilePath = os.path.join(dataOutputDir, f'{type}.csv')
    data_df.to_csv(dataFilePath, index=False)

    return dataFilePath

# Run the dataset converter. Function made for access from an API
def run(dataFileName, testDataFileName, output_dir: str, target: str, metric: str, tasks: list, tf_format: bool = False):
    global TF_TESTDIR, TF_TRAINDIR
    TF_TESTDIR = testDataFileName
    TF_TRAINDIR = dataFileName

    # Create output directory
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if tf_format and not os.path.isdir(dataFileName):
        raise RuntimeError(f"Inputs were specified to be tensorflow formatted directories, but provided input {dataFileName} is a file")
    if tf_format and not os.path.isdir(testDataFileName):
        raise RuntimeError(f"Inputs were specified to be tensorflow formatted directories, but provided input {testDataFileName} is a file")

    # If input is data in tensorflow format, create train and test dataFiles
    if tf_format:
        dataFileName = create_dataFiles(dataFileName, output_dir, type='train')
        testDataFileName = create_dataFiles(testDataFileName, output_dir, type='test')

    TRAIN_DATASET_PATH = f'{output_dir}/TRAIN/dataset_TRAIN/'
    TRAIN_PROBLEM_PATH = f'{output_dir}/TRAIN/problem_TRAIN/'
    TEST_DATASET_PATH = f'{output_dir}/TEST/dataset_TEST/'
    TEST_PROBLEM_PATH = f'{output_dir}/TEST/problem_TEST/'

    basic_json_problem["inputs"]["data"][0]['targets'][0]['colName'] = target
    basic_json_problem["inputs"]['performanceMetrics'][0]['metric'] = metric
    basic_json_problem["about"]['taskKeywords'] = []
    for t in tasks:
        basic_json_problem["about"]['taskKeywords'].append(t)
    
    print("Going to create TRAIN files!")
    create_directories(TRAIN_DATASET_PATH, TRAIN_PROBLEM_PATH, dataFileName, target, basic_json_problem)
    print("Going to create TEST files!")
    create_directories(TEST_DATASET_PATH, TEST_PROBLEM_PATH, testDataFileName, target, basic_json_problem)

    process_tasks(tasks, TRAIN_DATASET_PATH, TEST_DATASET_PATH, tf_format)

    logging.info(f'TRAIN and TEST directories can be found at: {output_dir}')


def main():
    # Available are the following parameters-
    # Metrics to use are - accuracy, f1Macro, f1Micro, rocAuc, rocAucMacro, rocAucMicro, 
    #                      rSquared, meanSquaredError, meanSquaredError, meanAbsoluteError, 
    #                      normalizedMutualInformation
    # Tasks to use are : video, linkPrediction, graphMatching, forecasting, classification, graph, semiSupervised, text, timeSeries, 
    #                    clustering, collaborativeFiltering, regression, audio, objectDetection, vertexNomination, communityDetection, image, 
    #                    vertexClassification

    # python create_d3m_dataset.py <dataFileName> <testDataFileName> <target> <metric> -t/--tasks
    # Sample command to use: python create_d3m_dataset.py data.csv data.csv Hall_of_Fame f1Macro -t classification -t tabular

    parser = argparse.ArgumentParser(description="Raw dataset specifications")
    parser.add_argument("dataTrain", type=str, help="dataset TRAIN filename")
    parser.add_argument("dataTest", type=str, help="dataset TEST filename")
    parser.add_argument("target", type=str, help="Target")
    parser.add_argument("metric", type=str, help="Metric")
    parser.add_argument('-o', '--output',type=str, required=False, default='raw', help='Output directory')
    parser.add_argument('-t','--tasks', action='append', help='Task(s)', required=True)
    parser.add_argument('--tf', action='store_true', help="Indicate if the input test and train are tensorflow format directories instead of train/test CSV files")
    args = parser.parse_args()
    print(args)

    if not os.path.exists(args.dataFileName):
        raise FileNotFoundError(f'Train data {args.dataFileName} does not exist')
    elif not os.path.exists(args.testDataFileName):
        raise FileNotFoundError(f'Test data {args.testDataFileName} does not exist')

    run(dataFileName=args.dataTrain, testDataFileName=args.dataTest, 
        output_dir=args.output, target=args.target, metric=args.metric, 
        tasks=args.tasks, tf_format=args.tf)

if __name__=="__main__":
    main()
