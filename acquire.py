import pandas as pd
import os
from env import get_db_url


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