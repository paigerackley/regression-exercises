# wrangle
from acquire import get_zillow_data
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings("ignore")

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