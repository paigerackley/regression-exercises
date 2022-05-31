import pandas as pd
import os
from env import get_db_url

###### ACQUIRE ###########

def get_zillow_data():
    filename = 'zillow_data.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col=0)
    else:
        df = pd.read_sql(
            '''
            SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips FROM properties_2017 WHERE propertylandusetypeid = 261; 
            '''
            ,
            get_db_url('zillow')
        )

        df.to_csv(filename)

        return df
######### PREPARE #############


def wrangle_zillow():
    '''
    Acquires and prepares zillow data for exploration and modeling
    '''
    # Pull data using an acquire function
    df = get_zillow_data()

    # Drop all nulls from dataset
    df = df.dropna()

    # Convert to integers where we can
    df = df.astype({'bedroomcnt':'int', 'calculatedfinishedsquarefeet':'int', 'taxvaluedollarcnt':'int', 'yearbuilt':'int', 'taxamount':'int','fips':'int'})

    # Eliminate the funky values
    df = df[df['calculatedfinishedsquarefeet'] > 400]
    df = df[df['taxvaluedollarcnt'] > 10000]
    df = df[df['taxamount'] > 200]

    return df