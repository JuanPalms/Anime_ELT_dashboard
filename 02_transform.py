import os
import pandas as pd

import src.web_scrapping as ws
import src.utils as ut
#configuring 
# config file loading
config_f = ws.config_f

# Relative paths
ROOT = ut.ROOT
DATA_PATH = os.path.join(ROOT, config_f['data']['raw']['secondary'])
OUT_PATH = 'data/transform/'

# Get scrapped data
df_ = pd.read_csv(DATA_PATH)

# Dataset column names format
df_.columns = ['_'.join(col_.split(sep=' ')).lower() for col_ in df_.columns]

# Convenient dataset content tranformations
df_processed = (
    df_
    .copy()
    
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
            .fillna(value='not_available')
            # Replace whitespace with '_' in column
            .apply(ut.format_list_str))
        
        # GENRES column in snake case
        ,genres = lambda df_: (
            df_
            .genres
            # Handle nan's
            .fillna(value='not_available')
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
    )
    
    # Add computed columns
    .assign(
    
        # EMISSION_TYPE column in snake case
        emission_type = lambda df_: (
            df_
            .number_of_episodes
            # Extract emission type info from column
            .str.partition(' ')[0]
            # Handle nan's
            .fillna(value='not_available')
            # Replace whitespace with '_' in column
            .apply(ut.format_single_str)
            # Remove abnormal characters in column
            .apply(ut.global_format))

        # NUMBER_EPISODES in numeric format
        ,number_episodes = lambda df_: (
            df_
            .number_of_episodes
            # Extract episodes info from column
            .str.partition(' ')[2]
            # Extract numeric value from string
            .str.extract(r'(\d+)')
            # Convert column type
            .astype(float)
        )

        # MEMBERS in numeric format
        ,members = lambda df_: (
            df_
            .number_members
            # Format 0,000 type number to 0000 in str
            .str.replace(',','')
            # Extract members info from column
            .str.partition(' ')[0]
            # Convert number str to float to include NAN's
            .astype(float))

        # FIRST_EMISSION as datetime
        ,first_emission = lambda df_: pd.to_datetime(
            df_
            .emission_date
            # Extract first emission info from column
            .str.split(' - ', expand=True)[0]
            # Coerce date str to datetime
            ,format='%b %Y'
            ,errors='coerce')
        
        # LAST_EMISSION as datetime
        ,last_emission = lambda df_: pd.to_datetime(
            df_
            .emission_date
            # Extract last emission info from column
            .str.split(' - ', expand=True)[1]
            # Coerce date str to datetime
            ,format='%b %Y'
            ,errors='coerce')

        # Extract year from emission date
        ,year = lambda df_: df_.first_emission.dt.year

        # Extract month from emission date
        ,month = lambda df_: df_.first_emission.dt.month
    )

    # Drop redundant columns
    .drop(columns=['number_of_episodes','emission_date','number_members'])
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
