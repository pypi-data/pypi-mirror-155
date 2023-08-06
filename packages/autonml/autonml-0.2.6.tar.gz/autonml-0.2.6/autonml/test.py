import os, logging, json
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score
from IPython.display import display

#from autonml import AutonML, createD3mDataset
import sys
sys.path.append('../autonml/')
from autonml_api import AutonML
from create_d3m_dataset import run

logging.basicConfig(level=logging.INFO)

# Substitute dataset and output parent directories here

dataset_dir = '/home/vsanil/projects/d3m/datasets/LL0_jido_reduced_MIN_METADATA'
output_par_dir = '/home/vsanil/projects/d3m/devel/cmu-ta2/output'

aml = AutonML(input_dir=dataset_dir,
             output_dir=output_par_dir,
             timeout=2, numcpus=8)

aml.run(metric='rocAuc')