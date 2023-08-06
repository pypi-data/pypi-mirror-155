from google.cloud import storage
from airflow.models import Variable
from datetime import datetime
import json
from dask import dataframe as dd


def create_dask_df(database=None,
                   table=None,
                   gcs_bucket=None):

    curr_date = datetime.now().strftime('%Y-%m-%d')
    filename = f'{table}-extract-{curr_date}.csv'

    data_folder = Variable.get('data_folder')
    data_path = f'{data_folder}/{database}/{table}/{filename}'

    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(f'schemas/{database}-{table}-dask-schema.json')
    dt_blob = blob.download_as_text()
    data_types = json.loads(dt_blob)

    ddf = dd.read_csv(data_path, delimiter='|', dtype=data_types)
    return ddf
