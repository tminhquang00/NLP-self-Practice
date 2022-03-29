#######################################################################################
## Author:          Phan Thanh Trung, Phan Ngoc Hung, Pham Nguyen Quang Khanh
##                  Tran Minh Quang, Dang Lam Tung
## Project:         [BGSV-HR-Chatbot]-Develop Chatbot for HR support
## Version:         4.0.0
## Maintainer:      Phan Ngoc Hung, Pham Nguyen Quang Khanh, Tran Minh Quang, Dang Lam Tung
## Status:          Work in Development and Maintenance
## Last modified:   March 17, 2022
## License:     
##    Copyright 2022, Robert Bosch Engineering & Business Solutions (RBVH)
## 
##    Licensed under the Apache License, Version 2.0 (the "License");
##    you may not use this file except in compliance with the License.
##    You may obtain a copy of the License at
## 
##        http://www.apache.org/licenses/LICENSE-2.0
##
##    Unless required by applicable law or agreed to in writing, software
##    distributed under the License is distributed on an "AS IS" BASIS,
##    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##    See the License for the specific language governing permissions and
##    limitations under the License.
#######################################################################################

import os
from sklearn import model_selection
import pandas as pd
import uuid

def read_data(path_to_data_file, columns_to_drop=[], columns_to_rename = {}):
    """Read data from csv file with pandas and handle column preprocessing
    Args:
        path_to_data_file:      str
            the file to csv data file
        columns_to_drop:        List[str]
            the list of column indices that are needed to drop
        columns_to_drop:        Dict
            the dict of old and new column name that are needed to apply
    Returns:
        pandas.core.frame.DataFrame
            the dataframe containing data
    """
    
    # Read data as csv format into pandas dataframe
    dataframe = pd.read_csv(path_to_data_file, encoding = "utf-8")

    # Drop unnecessary columns
    for column_name in columns_to_drop:
        if column_name in list(dataframe.columns):
            del dataframe[column_name]

    # Rename the columns    
    dataframe.rename(columns_to_rename, axis=1, inplace=True)

    return dataframe

def read_data_from_excel(path_to_data_file):
    """Read dataframe from excel file
    Args:
        path_to_data_file   : str
    
    Returns:
        pandas.DataFrame
            the dataframe of data read from excel file
    """
    return pd.read_excel(path_to_data_file)

def split_validation_data_by_index(index_lst, stratify_values, test_ratio=0.2):
    """Split data for training/testing validation purpose
        This function will be extended if there is any more splitting methods
    
    Args:
        data_x:         : List
            The list of input records in the dataset
        data_y:         : List
            The list of labelled records in the dataset
        test_ratio:     : float
            The ratio of testing data in the dataset
    Returns:
        List(), List(), List(), List()
            the corresponding lists of x_train, x_test, y_train, y_test

    """

    # Split the data into train:test using stratify splitting
    idx_train, idx_test = model_selection.train_test_split(
        index_lst, 
        test_size = test_ratio,
        stratify = stratify_values
    )

    return idx_train, idx_test

def exec_sys_cmd(cmd: str):
    os.system(cmd)

def create_random_uuid():
    """Generate random uuid by uuid 
    """
    return uuid.uuid1().hex

