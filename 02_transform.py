import os
import pandas as pd

import src.web_scrapping as ws
import src.utils as ut

# config file loading
config_f = ws.config_f

# Relative paths
ROOT = ut.ROOT
DATA_PATH = os.path.join(ROOT, config_f['data']['clean']['pre_clean'])
OUT_PATH = 'data/transform/'

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
            .apply(ut.format_single_str)
            # Remove abnormal characters in column
            .apply(ut.global_format))
        
        # THEMES column in snake case
        ,themes = lambda df_: (
            df_.
            themes
            # Handle nan's
            .fillna(value="['not_available']")
            # Replace whitespace with '_' in column
            .apply(ut.format_list_str))
        
        # GENRES column in snake case
        ,genres = lambda df_: (
            df_
            .genres
            # Handle nan's
            .fillna(value="['not_available']")
            # Replace whitespace with '_' in column
            .apply(ut.format_list_str))
        
        # DEMOGRAPHICS column in snake case
        ,demographics = lambda df_: (
            df_
            .demographics
            # Handle nan's
            .fillna(value='not_available')
            # Replace whitespace with '_' in column
            .apply(ut.format_single_str)
            # Remove abnormal characters in column
            .apply(ut.global_format))
        
        # EMISSION_TYPE column in snake case
        ,emission_type = lambda df_: (
            df_
            .emission_type
            # Handle nan's
            .fillna(value='not_available')
            # Replace whitespace with '_' in column
            .apply(ut.format_single_str)
            # Remove abnormal characters in column
            .apply(ut.global_format))
        
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
catalogs = ws.build_catalog(
    df_=df_processed
    ,columns=['themes','genres']
    ,count=True)

# Save transformed anime data
df_processed.to_csv(
    config_f['data']['transform']['main']
    ,index=False)

# Save catalogs
for cat_ in catalogs:
    # Extract catalog name from dictionary
    col_ = list(cat_.keys())[0]
    # Convert catalog content to dataframe
    cat_ = pd.DataFrame(cat_[col_])
    # Generate file name
    name = f'cat_{col_}.csv'
    # Save output data
    cat_.to_csv(
        os.path.join(OUT_PATH, name)
        ,index_label='id')


if __name__ == '__main__':
    print('Job done')