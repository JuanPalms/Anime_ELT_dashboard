"""
This python module load the processed data to S3 buckets
"""

import boto3
import pandas as pd
from utils import load_config
import os

CURRENT = os.getcwd()
ROOT = os.path.dirname(CURRENT)
######### LOAD #######

# Load config file calling load_config function
config_f = load_config("config.yaml")

session = boto3.Session(profile_name=config_f["AWS_config"]["PROFILE_NAME"])
s3 = boto3.client('s3')

# Crea un nuevo Bucket
BUCKET_NAME = config_f["AWS_config"]["BUCKET_NAME"]
s3.create_bucket(Bucket=BUCKET_NAME)

s3.upload_file(Filename=os.path.join(ROOT,config_f["data"]["transform"]["main"]),
               Bucket=BUCKET_NAME, Key="data/anime_transform.csv")
s3.upload_file(Filename=os.path.join(ROOT,config_f["data"]["transform"]["cat_genres"]),
               Bucket=BUCKET_NAME, Key="data/cat_genres.csv")
s3.upload_file(Filename=os.path.join(ROOT,config_f["data"]["transform"]["cat_themes"]),
               Bucket=BUCKET_NAME, Key="data/cat_themes.csv")