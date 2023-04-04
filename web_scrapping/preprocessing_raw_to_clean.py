"""
This python module uses as input the complete anime data and produces a clean data set ready to analyse. 
"""
import pandas as pd
import numpy as np
import os
from outils import load_config

# Load config file calling load_config function
config_f = load_config("config.yaml")

top_anime = pd.read_csv(os.path.join(config_f["data_directory"]+config_f["raw_data"],"raw_anime_principal_and_secondary_pages.csv"))

top_anime = (
    top_anime
        .assign(
            type_of_emission = lambda df_: df_['number_of_episodes'].str.extract(r'(\D+)'),
            emission_type = lambda df_: df_['type_of_emission'].str.replace('(', '', regex=True),
            number_episode = lambda df_: df_['number_of_episodes'].str.extract(r'(\d+)'),
            miembros = lambda df_: df_['number_members'].str.replace('members', '', regex=True),
            members = lambda df_: df_['miembros'].str.replace(',', '', regex=True)
        #end assign
        )
        .drop(columns= ['number_of_episodes','type_of_emission','miembros','number_members'])
    #end preprocessing
    )

# Split the 'emission_date' column into two new columns using the ' - ' delimiter
split_columns = top_anime['emission_date'].str.split(' - ', expand=True)

top_anime = (
    top_anime
        .assign(
            # Assign the new columns to the original DataFrame with the desired names
            first_emission = split_columns[0],
            last_emission  = split_columns[1],
            #ist_emission = lambda df_:df_['first_emission_y'].to_datetime(format='%b %Y')
            #df['last_emission'] = pd.to_datetime(df['last_emission'], format='%b %Y')
        ))


top_anime['first_emission'] = pd.to_datetime(top_anime['first_emission'], format='%b %Y', errors='coerce')
top_anime['last_emission'] = pd.to_datetime(top_anime['last_emission'], format='%b %Y', errors='coerce')


# Split the strings in 'themes' and 'genres' columns into lists
top_anime['themes'] = top_anime['themes'].fillna('Not_available').apply(lambda x: x.split(', ') if x else [])
top_anime['genres'] = top_anime['genres'].fillna('Not_available').apply(lambda x: x.split(', ') if x else [])

# Perform one-hot encoding for 'themes' and 'genres'
themes_dummies = pd.get_dummies(top_anime['themes'].apply(pd.Series).stack()).sum(level=0)
genres_dummies = pd.get_dummies(top_anime['genres'].apply(pd.Series).stack()).sum(level=0)



# Concatenate the one-hot encoded columns with the original DataFrame
result_df = pd.concat([top_anime, themes_dummies, genres_dummies], axis=1)
print(result_df.head())




result_df.to_csv(os.path.join(config_f["data_directory"]+config_f["clean_data"],"anime_data_clean.csv"),index=False)
