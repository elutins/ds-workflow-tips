from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split


def assign_dummies(data):
    dummies = [
        'hotel',
        'arrival_date_year',
        'arrival_date_month',
        'meal',
        'country',
        'market_segment',
        'distribution_channel',
        'reserved_room_type',
        'assigned_room_type',
        'deposit_type',
        'customer_type',
        ]
    
    data = pd.get_dummies(data, columns=dummies, dtype=np.int64)

    return data


def check_value(row, values):
    count = 0
    for v in values:
        if str(row) in v:
            count += 1
            break

    return int(count == 0)


def crosscheck_dummies(fields: list, train_data: any, test_data: any):
    data = {}
    vals = set(train_data)

    for col in fields:
        logger.debug("checking if test field value existed in training", col=col)
        new_field = test_data[col].apply(lambda row: check_value(row, vals))
        name = col + "_other"
        data[name] = new_field

    return pd.DataFrame(data)


def crosscheck_testing_fields(test_data: pd.DataFrame, training_fields: list):
    """
    Assures all training fields appear in test set.
    If training field is not in test set, create a new series of all 0s 
    
    :params:
        test_data: pd.DataFrame of test set after transformation/categorical variables have been encoded
        training_fields: list of fields that were in training set

    :returns:
        pd.DataFrame of test set with appended series
    """
    data = test_data.copy()

    for field in training_fields:
        if field not in data.columns:
            data[field] = 0

    return data


def transform_data(data, training_flag: bool=False):

    df = data.copy()

    # printing out value counts of target field to get a baseline score
    # print("baseline score")
    # print(df.is_canceled.value_counts(normalize=True))

    #  dropping rows where children are null -- 4 in total
    df.dropna(subset=['children'], axis=0, inplace=True)
    df = assign_dummies(df)

    # 94% of company field is null, 14% of agent field null. dropping both for this case
    fields_to_drop = ['company', 'agent', 'reservation_status', 'reservation_status_date']
    if not training_flag:
        # if predicting, will want to drop target field from data as well
        fields_to_drop += ['is_canceled']
        
    df.drop(fields_to_drop, axis=1, inplace=True)

    return df

def generate_test_train_sets(data, field):

    X = data.drop(labels=field, axis=1)
    y = data[field]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    return X_train, X_test, y_train, y_test


def ensure_file_path(raw_path):
    path = Path(raw_path)
    path.mkdir(parents=True, exist_ok=True)





 
