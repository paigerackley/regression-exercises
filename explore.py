import wrangle
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations, product


def plot_variable_pairs(df,
                        columns_x = ['bedroomcnt','bathroomcnt','square_feet','yearbuilt','taxvaluedollarcnt','taxamount'],
                        columns_y = ['bedroomcnt','bathroomcnt','square_feet','yearbuilt','taxvaluedollarcnt','taxamount'],
                        sampling = 1000):
    pairs = product(columns_x, columns_y)
    for pair in pairs:
        sns.lmplot(x=pair[0], y=pair[1], data=df.sample(sampling), line_kws={'color': 'blue'})
        plt.show()





def plot_categorical_and_continuous_vars(df,
                                         columns_cat=['fips_name'],
                                         columns_cont=['square_feet', 'yearbuilt', 'bedroomcnt', 'bathroomcnt', 
                                         'taxvaluedollarcnt', 'taxamount'],
                                         sampling = 1000):
    pairs = product(columns_cat, columns_cont)
    for pair in pairs:
        sns.set(rc={"figure.figsize":(15, 6)}) 
        fig, axes = plt.subplots(1, 3)

        sns.stripplot(x=pair[0], y=pair[1], data=df.sample(sampling), ax = axes[0])
        sns.boxplot(x=pair[0], y=pair[1], data=df.sample(sampling), ax = axes[1])
        sns.barplot(x=pair[0], y=pair[1], data=df.sample(sampling), ax = axes[2])

        plt.show