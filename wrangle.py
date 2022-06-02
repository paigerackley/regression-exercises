import pandas as pd
import os
from env import get_db_url
#### ACQUIRE ######

"""
USAGE: 
Use `from wrangle import wrangle_zillow` at the top of your notebook.
This 
"""
def get_zillow_data():
    """Seeks to read the cached zillow.csv first """
    filename = "zillow.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        return get_new_zillow_data()

def get_new_zillow_data():
    """Returns a dataframe of all 2017 properties that are Single Family Residential"""

    sql = """
    select 
    bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    from properties_2017
    join propertylandusetype using (propertylandusetypeid)
    where propertylandusedesc = "Single Family Residential"
    """
    return pd.read_sql(sql, get_db_url("zillow"))

    ###########################


def wrangle_zillow():
    """
    Acquires Zillow data
    Handles nulls
    optimizes or fixes data types
    handles outliers w/ manual logic
    returns a clean dataframe
    """
    df = get_zillow_data()

    # Drop all nulls from dataset

    # Convert some columns to integers
    # fips, yearbuilt, and bedrooms can be integers
    df["fips"] = df["fips"].astype(int)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)    
    df["taxvaluedollarcnt"] = df["taxvaluedollarcnt"].astype(int)
    df["calculatedfinishedsquarefeet"] = df["calculatedfinishedsquarefeet"].astype(int)
    df = df.dropna()

    # readability
    df = df.rename(columns={'calculatedfinishedsquarefeet': 'sqr_ft'})

    # Eliminate the funky values
    df = df[df['calculatedfinishedsquarefeet'] > 400]
    df = df[df['calculatedfinishedsquarefeet'] < 100000]
    df = df[df['taxvaluedollarcnt'] > 10000]
    df = df[df['taxvaluedollarcnt'] < 20000000]
    df = df[df['taxamount'] > 100]
    df = df[df['taxamount'] < 300000]
    df = df[df['bathroomcnt'] > 0]
    df = df[df['bedroomcnt'] > 0]
    df = df[df['bathroomcnt'] < 7]
    df = df[df['bedroomcnt'] < 7]

    return df

### SPLIT #####
def train_validate_test_split(df, target, seed=123):
    '''
    This function takes in a dataframe, the name of the target variable, and an integer for a setting a seed
    and splits the data into train, validate and test.
    Test is 20% of the original dataset, validate is .30*.80= 24% of the
    original dataset, and train is .70*.80= 56% of the original dataset.
    The function returns, in this order, train, validate and test dataframes.
    '''
    train_validate, test = train_test_split(df, test_size=0.2,
                                            random_state=seed)
    train, validate = train_test_split(train_validate, test_size=0.3,
                                       random_state=seed)
    return train, validate, test

#### Scale #####
