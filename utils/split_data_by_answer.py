import pandas as pd

import utils

# Pre-define params (need to put in config file in the future)
DATA_FILE = '../data/data_ver3.0/HR_Chatbot_data_3.0.csv'
COLUMNS_TO_RENAME = {
    'questions': 'Question', 
    'labels': 'Label',
    'answers': 'Answer',
    'answers_id': 'Ans_id'
}


def read_dataframe(data_path, columns_to_drop=[], columns_to_rename={}):

    df = utils.read_data(
        path_to_data_file = data_path,
        columns_to_drop   = columns_to_drop,
        columns_to_rename = columns_to_rename
    )

    # Drop rows wherer Label and Question are NaN
    df = df[(df['Label'].notna()) & (df['Question'].notna())]

    return df

if __name__ == '__main__':

    # Read dataframe from csv   
    df = read_dataframe(
        DATA_FILE,
        # COLUMNS_TO_DROP,
       columns_to_rename=COLUMNS_TO_RENAME
    )

    # Extract questions, answer and intent labels in 3 lists
    questions = df['Question'].tolist()
    answers   = df['Answer'].tolist()
    labels    = df['Label'].tolist()
    ans_id    = df['Ans_id'].tolist()

    ################################################################
    # SPLIT DATA INTO TRAIN/TEST PARTITIONS 
    ################################################################

    # Train/Test split data
    index_lst = list(range(len(df)))

    # Stratified split indices into Train/Test set
    indices_train, indices_test = utils.split_validation_data_by_index(
        index_lst = index_lst,
        stratify_values = answers,
        test_ratio=0.2
    )

    # Sub-sampling data using index lists
    df_train = df.iloc[indices_train, :]
    df_test = df.iloc[indices_test, :]

    # Export to csv
    df_train.to_csv('../data/data_ver3.0/HR_Chatbot_data_train.csv', index=False)
    df_test.to_csv('../data/data_ver3.0/HR_Chatbot_data_test.csv', index=False)
