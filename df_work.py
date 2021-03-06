import pandas as pd

def listCriticalAssets(df, CRITICAL_STATUS):
    """
    takes in dataframe generated by the http .txt file and lists all assets
    that are in critical condition
    """
    # df of all critical assets
    crit_assets = df.loc[df['status']==CRITICAL_STATUS, ['assetId', 'name', 'description', 'status', 'Location.propertyId', 'Location.value']]
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(crit_assets)



def searchTopLevel(df):
    """
    take in user input as to which category to index by then prompt user to
    select what information in that category they would like to index by
    """
    print('Which category would you like to index by?')
    cat = input()
    cat = cat.strip()
    while( cat not in df ):
        print('Invalid top level category, please try again.')
        print('Make sure it is formatted correctly')
        cat = input()

    print('What would you like to see in this category?')
    val = input()

    # have to get the value in the right datatype for the category
    g = df.columns.to_series().groupby(df.dtypes).groups
    dtype_key = {k.name: v for k, v in g.items()}
    int_cats = []
    for i in dtype_key['int64']:
        int_cats.append(i) # add the categories that are int64 format
    for j in dtype_key['float64']:
        int_cats.append(j) # add the columns that are floats
    if cat in int_cats:  # if the selected column is supposed to be an int/float
        val = int(val)

    if cat in ['classList.id', 'classList.name', 'classList.drill']: # these are lists, have to treat it differently
        bool_series = []
        if cat == 'classList.id': val = int(val)
        for i in df[cat]:
            if val in i:
                bool_series.append(True)
            else:
                bool_series.append(False)
        indexed_df = df.loc[bool_series, [cat, 'assetId', 'name', 'description', 'status']]
    else:
        indexed_df = df.loc[df[cat] == val, [cat, 'assetId', 'name', 'description', 'status']]
    # print out all the data
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(indexed_df)




def uniqueClass(df):
    """room for optimization: builds list of unique class names, as well as
       list of names of assets that correspond to each class name simultaneously"""
    unique_classes = []
    assets = {}
    for index, row in df.iterrows():
        for name in row['classList.name']:
            if name not in unique_classes:
                unique_classes.append(name)
                assets[name] = [row['name']]
            else:
                assets[name].append(row['name'])

    print("There are ", len(unique_classes), "unique classes")
    for key in assets:
        print(key, ": ", assets[key], '\n\n')
