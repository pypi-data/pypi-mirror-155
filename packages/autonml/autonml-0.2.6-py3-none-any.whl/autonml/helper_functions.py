
import os, time, random, copy, logging, typing, math, subprocess
from enum import Enum
from google.protobuf.timestamp_pb2 import Timestamp
import numpy as np
import pandas as pd
import d3m.index
from timeit import default_timer as timer
from d3m.metadata import base as metadata_base

# AutonML imports
import autonml.value_pb2 as value_pb2

def get_argument(data):
    """
    Split string into origin and source for pipeline construction
    """
    origin = data.split('.')[0]
    source = data.split('.')[1]
    return {'origin': origin, 'source': int(source), 'data': data}

def isFloat(value):
    """
    Is a float?
    """
    try:
        a  = float(value)
        return True
    except:
        return False

def isOrdinal(df, t):
    """
    Whether a categorical attribute needs to be treated as ordinal?
    """
    missing = 0
    if df.dtypes[t] == 'object':
        missing = len(np.where(df.iloc[:,t] == '')[0])
        if missing == 0:
            try:
                pd.to_numeric(df.iloc[:,t])
                return True
            except:
                print("Att ", df.columns[t], " non-numeric")
    return False

def isNumeric(df, t):
    """
    Is a numeric attribute?
    """
    anynumber = False
    try:
        for i in range(5):
            if isFloat(df.iloc[i,t]) is True:
                anynumber = True
                break
    except:
        print("Att ", df.columns[t], " non-numeric")
    return anynumber

def compute_timestamp():
    now = time.time()
    seconds = int(now)
    return Timestamp(seconds=seconds)

class StepType(Enum):
    PRIMITIVE = 1
    SUBPIPELINE = 2
    PLACEHOLDER = 3

class ActionType(Enum):
    FIT = 1
    SCORE = 2
    VALIDATE = 3

def get_values(arg):
    value = None
    if arg.HasField("double") == True:
        value = arg.double
    elif arg.HasField("int64") == True:
        value = arg.int64
    elif arg.HasField("bool") == True:
        value = arg.bool
    elif arg.HasField("string") == True:
        value = arg.string
    elif arg.HasField("bytes") == True:
        value = arg.bytes
    elif arg.HasField("list") == True:
        value = get_list_items(arg.list.items)
    elif arg.HasField("dict") == True:
        value = get_dict_items(arg.dict.items)

    return value

def get_list_items(values : value_pb2.ValueList):
    items = []

    for i in values:
        items.append(get_values(i))

    return items

def get_dict_items(values : value_pb2.ValueDict):
    items = {}

    for name, arg in values.items():
        items[name] = get_values(arg)
    return items

def get_pipeline_values(value):
    if value is None:
        return value_pb2.Value(raw=value_pb2.ValueRaw(null=value_pb2.NULL_VALUE))
    if isinstance(value, list):
        vitems = []
        for v in value:
            vitems.append(get_pipeline_values(v).raw)
        vlist = value_pb2.ValueList(items=vitems)
        return value_pb2.Value(raw=value_pb2.ValueRaw(list=vlist))
    elif isinstance(value, dict):
        vitems = {}
        for name,v in value.items():
            vitems[name] = get_pipeline_values(v).raw
        vlist = value_pb2.ValueDict(items=vitems)
        return value_pb2.Value(raw=value_pb2.ValueRaw(dict=vlist))
    elif isinstance(value, bool):
        return value_pb2.Value(raw=value_pb2.ValueRaw(bool=value))
    elif isinstance(value, int):
        return value_pb2.Value(raw=value_pb2.ValueRaw(int64=value))
    elif isinstance(value, float):
        return value_pb2.Value(raw=value_pb2.ValueRaw(double=value))
    elif isinstance(value, str):
        return value_pb2.Value(raw=value_pb2.ValueRaw(string=value))
    return None

def get_cols_to_encode(df):
    """
    Find categorical attributes which can be one-hot-encoded.
    Find categorical attributes which can be treated as ordinals.
    Find attributes of UnknownType which can be treated as floats.
    """
    cols = df.metadata.get_columns_with_semantic_type("https://metadata.datadrivendiscovery.org/types/CategoricalData")
    targets = df.metadata.get_columns_with_semantic_type("https://metadata.datadrivendiscovery.org/types/TrueTarget")
    attributes = df.metadata.get_columns_with_semantic_type("https://metadata.datadrivendiscovery.org/types/Attribute")

    for t in targets:
        if t in cols:
            cols.remove(t)

    rows = len(df)
    # use rule of thumb to exclude categorical atts with high cardinality for one-hot-encoding
    max_num_cols = math.log(rows, 2)
    if len(attributes) >= 100 and max_num_cols > 0.05*len(attributes):
        max_num_cols = 0.05*len(attributes)

    if rows > 100000:
        max_num_cols = max_num_cols/4

    tmp_cols = copy.deepcopy(cols)
    ordinals = []

    # Iterate over all categorical attributes
    for t in tmp_cols:
        if isFloat(t) == False:
            cols.remove(t)
            continue

        arity = len(df.iloc[:,t].unique())
        if arity == 1:
            cols.remove(t)
            continue

        if arity > max_num_cols:
            cols.remove(t)
            if isOrdinal(df, t) is True:
                ordinals.append(t)
        elif rows > 1000000 and isOrdinal(df, t) is True:
            cols.remove(t)
            ordinals.append(t)

    if rows > 100000 and len(cols) > 5:
        cols = random.sample(cols, 5)

    add_floats = []
    for att in attributes:
        md = df.metadata.query((metadata_base.ALL_ELEMENTS, att))
        if md['structural_type'] != str:
            continue

        if 'semantic_types' not in md:
            continue

        attmeta = md['semantic_types']
        length = len(attmeta)-1
        if 'https://metadata.datadrivendiscovery.org/types/UniqueKey' in attmeta:
            continue
        if 'https://metadata.datadrivendiscovery.org/types/UnknownType' in attmeta:
            length = length-1
        if length == 0:
            anynumber = isNumeric(df, att)
            if anynumber is True:
                logging.critical("Float for %s", att)
                add_floats.append(int(att))
    logging.info("No. of cats = %s", len(cols))
    logging.info("Floats = %s", add_floats)
    return (list(cols), ordinals, add_floats)

def get_primitive_volumes(volumes_dir, primitive_class, primitive_name="") -> typing.Dict:
        volumes = {}
        for entry in primitive_class.metadata.get_volumes():
            volume_path = os.path.join(volumes_dir, entry['file_digest'])
            if not os.path.exists(volume_path):
                subprocess.run(["python", "-m", "d3m", "primitive", "download", "-p", primitive_name, "-o", os.environ['D3MSTATICDIR']])
            volumes[entry['key']] = volume_path
        return volumes

def get_num_splits(length, cols):
    splits = 2
    if length < 500:
        splits = 50
        if length < splits:
            splits = length
    elif length < 1000:
        splits = 25
    elif length < 2500:
        splits = 20
    elif length < 5000:
        splits = 10
    elif length < 10000:
        splits = 5
    elif length < 20000:
        splits = 3
    else:
        splits = 2

    #if cols > 500:
    splits = min(5, splits)
    return splits

def get_split_indices(X, y, splits, python_path='classification'):
    if 'classification' in python_path: # Classification
        frequencies = y.iloc[:,0].value_counts()
        min_freq = frequencies.iat[len(frequencies)-1]
        if min_freq < splits:
            from sklearn.model_selection import KFold as KFold
            kf = KFold(n_splits=splits, shuffle=True, random_state=9001)
            split_indices = kf.split(X)
        else:
            from sklearn.model_selection import StratifiedKFold as KFold
            kf = KFold(n_splits=splits, shuffle=True, random_state=9001)
            split_indices = kf.split(X, y)
    else: # Regression
        from sklearn.model_selection import KFold as KFold
        kf = KFold(n_splits=splits, shuffle=True, random_state=9001)
        split_indices = kf.split(X)
    return split_indices

def column_types_present(dataset):
    """
    Retrieve special data types present: Text, Image, Timeseries, Audio, Categorical
    Returns ([data types], total columns, total rows, [categorical att indices], ok_to_denormalize, privileged, add_floats)
    """
    ok_to_denormalize = True
    start = timer()

    try:
        primitive = d3m.index.get_primitive('d3m.primitives.data_transformation.denormalize.Common')
        primitive_hyperparams = primitive.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
        model = primitive(hyperparams=primitive_hyperparams.defaults())
        ds = model.produce(inputs=dataset).value
        dataset = ds
    except:
        print("Exception with denormalize!")
        ok_to_denormalize = False

    primitive = d3m.index.get_primitive('d3m.primitives.data_transformation.dataset_to_dataframe.Common')
    primitive_hyperparams = primitive.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
    model = primitive(hyperparams=primitive_hyperparams.defaults())
    df = model.produce(inputs=dataset).value
    atts = df.metadata.get_columns_with_semantic_type('https://metadata.datadrivendiscovery.org/types/UnknownType')
    print("Dataset shape = ", len(df), ", ", len(df.columns))

    if len(df.columns) > 5000:
        return ([], len(df.columns), len(df), [], [], True, [], [])

    profiler_needed = False
    primitive = d3m.index.get_primitive('d3m.primitives.schema_discovery.profiler.Common')
    primitive_hyperparams = primitive.metadata.query()['primitive_code']['class_type_arguments']['Hyperparams']
    model = primitive(hyperparams=primitive_hyperparams.defaults())
    model.set_training_data(inputs=df)
    try:
        model.fit()
        df = model.produce(inputs=df).value
    except:
        profiler_needed = False

    metadata = df.metadata

    types = []
    (categoricals, ordinals, add_floats) = get_cols_to_encode(df)
    if len(categoricals) > 0:
        types.append('Categorical')
        logging.critical("Cats = %s", categoricals)
    if len(ordinals) > 0:
        types.append('Ordinals')
        print("Ordinals = ", ordinals)

    textcols = metadata.get_columns_with_semantic_type("http://schema.org/Text")
    if len(textcols) > 0:
        logging.critical("Text = %s", textcols)
        types.append('COREXTEXT')
    cols = len(metadata.get_columns_with_semantic_type("http://schema.org/ImageObject"))
    if cols > 0:
        types.append('IMAGE')
    cols = len(metadata.get_columns_with_semantic_type("https://metadata.datadrivendiscovery.org/types/Timeseries"))
    if cols > 0:
        types.append('TIMESERIES')
    cols = len(metadata.get_columns_with_semantic_type("http://schema.org/AudioObject"))
    if cols > 0:
        types.append('AUDIO')
    cols = len(metadata.get_columns_with_semantic_type("http://schema.org/VideoObject"))
    if cols > 0:
        types.append('VIDEO')
    cols = len(metadata.get_columns_with_semantic_type("https://metadata.datadrivendiscovery.org/types/FileName"))
    if cols > 0:
        types.append('FILES')

    privileged = metadata.get_columns_with_semantic_type("https://metadata.datadrivendiscovery.org/types/PrivilegedData")
    attcols = metadata.get_columns_with_semantic_type("https://metadata.datadrivendiscovery.org/types/Attribute")

    print("Data types present: ", types)
    end = timer()
    logging.critical("Time taken in determining data types: %f secs", (end-start))
    return (types, len(attcols), len(df), categoricals, ordinals, ok_to_denormalize, privileged, add_floats)

