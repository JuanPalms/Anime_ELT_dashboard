import os
import re
import pandas as pd

from ast import literal_eval


# Utils functions
def global_format(x):
    '''
    Remove atypical character from given string

    Params:
        x: String to format
    
    Returns:
        x: String without atypical characters
    '''
    x = re.sub(pattern=r"[°.-]+", repl='_', string=x)
    x = re.sub(pattern="'s", repl='', string=x)
    return x

# lambda function to format single string data in cell
format_single_str = lambda cel_: '_'.join(
    cel_.rstrip().lstrip().split(sep=' ')
).lower()

# lambda function to format list like data in cell
format_list_str = lambda cel_: [
    global_format(
        '_'.join(val_.split(' ')).lower()
    ) for val_ in literal_eval(cel_)
]


# Script functions
def build_catalog(df_, columns, count=True):
    '''
    Generate catalog of unique classes in column
    for given dataframe

    Params:
        df_: Dataframe
        columns: Columns to extract classes
        count: Whether to return value counts or not

    Returns:
        catalogs: List of dictionaries, length = len(columns)
        containing unique classes per column in dataframe
    '''
    # Generate list of catalogs to compute
    catalogs = [{col_:None} for col_ in columns]
    
    # Populate all catalogs
    for id_, col_ in enumerate(columns):
        
        # Empty list of tokens in catalog
        tokens = []
        
        # Append all existing tokens in column
        for val_ in df_[col_]:
            tokens += val_
        
        # Assign unique tokens in list to catalog
        if count:
            catalogs[id_][col_] = (
                # Convert tokens list to pandas series
                pd.Series(tokens)
                # Extract series value counts
                .value_counts()
                # Reset index to store tokens as dataframe
                .reset_index()
                # Rename columns with convenient names
                .rename(columns={'index':col_, 0:'count'})
                # Sort tokens alphabetically
                .sort_values(by=col_)
                # Reset dataframe index
                .reset_index(drop=True))
        else:
            catalogs[id_][col_] = (
                # Convert array to dataframe for manipulation
                pd.DataFrame(
                    # Convert tokens list to pandas series
                    pd.Series(tokens)
                    # Extract series unique values
                    .unique())
                # Rename columns with convenient names
                .rename(columns={0:col_})
                # Sort tokens alphabetically
                .sort_values(by=col_)
                # Reset dataframe index
                .reset_index(drop=True))
    
    return catalogs


# Relative paths
CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)
DATA_PATH = os.path.join(ROOT, 'data/clean/anime_data_clean.csv')
OUT_PATH = os.path.join(ROOT, 'data/transform/')

# Get scrapped data
df_ = pd.read_csv(DATA_PATH)

# Dataset column names format
df_.columns = ['_'.join(col_.split(sep=' ')).lower() for col_ in df_.columns]

# Convenient dataset content tranformations
df_processed = (
    df_
    .copy()
    
    # Ignore encoded columns
    .filter(items=df_.columns[0:13])
    
    # Transform existing columns
    .assign(
        
        # STUDIO column in snake case
        studio = lambda df_: (
            df_
            .studio
            # Handle nan's
            .fillna(value='not_available')
            # Replace whitespace with '_' in column
            .apply(format_single_str)
            # Remove abnormal characters in column
            .apply(global_format))
        
        # THEMES column in snake case
        ,themes = lambda df_: (
            df_.
            themes
            # Handle nan's
            .fillna(value="['not_available']")
            # Replace whitespace with '_' in column
            .apply(format_list_str))
        
        # GENRES column in snake case
        ,genres = lambda df_: (
            df_
            .genres
            # Handle nan's
            .fillna(value="['not_available']")
            # Replace whitespace with '_' in column
            .apply(format_list_str))
        
        # DEMOGRAPHICS column in snake case
        ,demographics = lambda df_: (
            df_
            .demographics
            # Handle nan's
            .fillna(value='not_available')
            # Replace whitespace with '_' in column
            .apply(format_single_str)
            # Remove abnormal characters in column
            .apply(global_format))
        
        # EMISSION_TYPE column in snake case
        ,emission_type = lambda df_: (
            df_
            .emission_type
            # Handle nan's
            .fillna(value='not_available')
            # Replace whitespace with '_' in column
            .apply(format_single_str)
            # Remove abnormal characters in column
            .apply(global_format))
        
        # FIRST_EMISSION as datetime
        ,first_emission = lambda df_: pd.to_datetime(df_.first_emission)
    )
    
    # Add computed columns
    .assign(
        # Extract year from emission date
        year = lambda df_: df_.first_emission.dt.year
        # Extract month from emission date
        ,month = lambda df_: df_.first_emission.dt.month
    )
)

# Generate catalogs
catalogs = build_catalog(
    df_=df_processed
    ,columns=['themes','genres']
    ,count=True)

# Save transformed anime data
df_processed.to_csv(
    os.path.join(OUT_PATH, 'anime_transform.csv')
    ,index=False)

# Save catalogs
for cat_ in catalogs:
    # Extract catalog name from dictionary
    col_ = list(cat_.keys())[0]
    # Convert catalog content to dataframe
    cat_ = pd.DataFrame(cat_[col_])
    # Generate file name
    name = f'cat_{col_}'
    # Save output data
    cat_.to_csv(
        os.path.join(OUT_PATH, name)
        ,index_label='id')


if __name__ == '__main__':
    print('Job done')