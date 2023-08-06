import joblib
import pandas                   as pd

from enum                       import Enum
from typing                     import Tuple, TypeVar
from sklearn                    import preprocessing

# Data analysis tools

## Auxiliar elements
class Scaler(Enum):
    MinMax      = preprocessing.MinMaxScaler()
    Standard    = preprocessing.StandardScaler()

## Dataset related tools
def show_columns_value(dataset:pd.DataFrame, cols_to_omit:list=[]) -> None:
    for column in list(dataset.columns):
    
        if (column not in cols_to_omit):
            print('Values in column {}:'.format(column))

            for value in dataset[column].unique():
                print('\t+ {}'.format(value))
        
def load_tables_from_big_JSON(database:str) -> list:
    dicts_dfs = []

    with open(database, 'rb') as fin:
        for obj in ijson.items(fin, 'item'):
            dicts_dfs.append(obj)

    return dicts_dfs

def show_columns_value(dataset:pd.DataFrame, cols_to_omit:list=[]) -> None:
    for column in list(dataset.columns):
    
        if (column not in cols_to_omit):
            print('Values in column {}:'.format(column))

            for value in dataset[column].unique():
                print('\t+ {}'.format(value))

def read_dataset(path:str, separator:str=",") -> pd.DataFrame:
    """ Reads the dataset in csv format by defect (separator = ,)
    
    Parameters:
    path (str):         String path to the file in order to read it.

    separator (str):    String character that separates the data's columns.

    Returns:
    pandas DataFrame object with all the registers from the file pass.

    """

    return pd.read_csv(path, sep=separator)

def clean_and_normalize_dataset(dataset:pd.DataFrame, exclude=[]) -> pd.DataFrame:
    """ Cleans and normalize the data from a pandas DataFrame object

    Parameters:
    data (DataFrame):   pandas DataFrame object with the data to normalize

    exclude (list):     List with integer data that represents the columns
                        of the dataset to be excluded from normalized.

    Returns:
    A panda DataFrame object with the data normalized and cleaned of the
    columns that are indicated in exclude list.

    """

    df_ex           = dataset.loc[:, dataset.columns.difference(exclude)]
    df_labels       = dataset[exclude]

    columns         = df_ex.columns
    old_indexes     = df_ex.index.values

    
    min_max_scaler  = preprocessing.MinMaxScaler()
    df_norm         = min_max_scaler.fit_transform(df_ex)
    
    df_norm = pd.DataFrame(df_norm, columns = columns, index = old_indexes)

    df_norm = pd.concat([df_norm, df_labels], axis=1)

    return df_norm

def normalize_dataset(dataset:pd.DataFrame, scaler:str='MinMax') -> pd.DataFrame:
    """ Just normalize all the data in a pandas DataFrame object

    Parameters:
    dataframe (DataFrame): pandas DataFrame object with the data to normalize
    scaler (str):          A string that choose one of the scalers in the enum Scaler

    Returns:
    A pandas object with the data normalized

    """
    try:
        scaler      = eval('Scaler.{}'.format(scaler))
    
    except Exception as e:
        print(e)
    
    norm_values = scaler.fit_transform(dataset)
    
    dataframe_norm  = pd.DataFrame(data=norm_values, columns=dataset.columns) 
     
    return dataframe_norm


def divide_datasets(df_merged:pd.DataFrame, percentage:float=0.67) -> Tuple[pd.DataFrame, pd.DataFrame]:
    
    df_divide = df_merged.sample(frac=1)
    df_train = df_divide[:int((len(df_divide))*percentage)]
    df_test = df_divide[int((len(df_divide))*percentage):]    
    
    return df_train, df_test

def divide_files(list_of_files:list, percentage:float=0.67) -> Tuple[list, list]:

    list_train  = []
    list_test   = []
    
    for i in range(len(list_of_files)):
        i_list = random.randint(1, 100)

        if i_list <= percentage * 100:
            list_train.append(list_of_files[i])
        else:
            list_test.append(list_of_files[i])

    return list_train, list_test

def insert_row_in_pos(pos:int, row_value:TypeVar('T'), dataset:pd.DataFrame) -> pd.DataFrame:
	# Funciona con objetos de tipo Series de pandas.

    data_half_low, data_half_big = dataset[:pos], dataset[pos:]
    data_half_low = data_half_low.append(row_value, ignore_index = True)
    data_half_low = data_half_low.append(data_half_big, ignore_index = True)
	
    return data_half_low

def merge_datasets_on_folder(data_folder:str, output_name:str) -> pd.DataFrame:
    
    datasets_list = ls(data_folder)
    
    data_to_combine = []
    
    for dataset_name in datasets_list:
        data_to_combine.append(pd.read_csv(data_folder+dataset_name))
        
    
    resume_dataset = pd.concat(data_to_combine)
    resume_dataset.to_csv(output_name)
    
    return resume_dataset

def compute_consecutive_parameters_aggregation(dataset:pd.DataFrame, column_name:str) -> pd.DataFrame:
    column_name_aux = column_name + '_X'
    dataset[column_name_aux] = dataset[column_name].shift()
    
    dataset["cumsum"] = (dataset[column_name] != dataset[column_name_aux]).cumsum()
    
    return dataset
    
def agrupate_by_cycles(dataset:pd.DataFrame, column_name:str, 
                       col_to_group:str, values_to_delimite:list) -> pd.DataFrame:  
    df_aux = dataset.groupby([col_to_group, 'cumsum']).first()
    df_aux['cycle'] = (df_aux[column_name].isin(values_to_delimite)).cumsum()
    
    
    df_aux2 = df_aux.groupby([col_to_group, 'cycle']).first()
        
    return df_aux2

## Decision tree and Random Forests related tools

def tree_to_code(tree, feature_names):
    
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print ("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print ("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            print ("{}return {}".format(indent, tree_.value[node]))

    recurse(0, 1)

## Machine learning models tools

def save_context(generic_object:TypeVar('T'), name:str, folder:str) -> None:
    # Save to file in the current working directory
    pkl_filename = "{}/{}".format(folder, name)  
    with open(pkl_filename, 'wb') as file:  
        joblib.dump(generic_object, file)
        
def load_context(name:str, folder:str) -> TypeVar('T'):
    # Save to file in the current working directory
    pkl_filename = "{}/{}".format(folder, name)  
    # Load from file
    with open(pkl_filename, 'rb') as file:  
        generic_object = joblib.load(file)
    
    return generic_object
    
def save_model(model:TypeVar('T'), test:pd.DataFrame, name:str, folder:str, feature_to_predict:str) -> None:
    
    features    = test.columns[:32]
    Xtest       = test[features]
    Ytest       = test[feature_to_predict]
    
    # Save to file in the current working directory
    pkl_filename = "{}/{}".format(folder, name)  
    with open(pkl_filename, 'wb') as file:  
        joblib.dump(model, file)
    
    # Load from file
    with open(pkl_filename, 'rb') as file:  
        joblib_model = joblib.load(file)
    
    # Calculate the accuracy score and predict target values
    score = joblib_model.score(Xtest, Ytest)  
    print("Test score: {0:.2f} %".format(100 * score))  
    
def load_model(joblib_file:TypeVar('T'), test:pd.DataFrame, feature_to_predict:int, acc_opt:int=-1) -> TypeVar('T'):
    
    if acc_opt == 0:
        features    = test.columns[:32]
        Xtest       = test[features]
        Ytest       = test[feature_to_predict]
            
        # Load from file
        joblib_model = joblib.load(joblib_file)
        
        # Calculate the accuracy and predictions
        score = joblib_model.score(Xtest, Ytest)  
        print("Test score: {0:.2f} %".format(100 * score))
        
        return joblib_model

    else:
        joblib_model = joblib.load(joblib_file)
        return joblib_model