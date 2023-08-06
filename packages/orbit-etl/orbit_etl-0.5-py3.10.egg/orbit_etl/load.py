from google.cloud import storage
from airflow.models import Variable
from datetime import datetime


def load_gcs(project=None,
             database=None,
             table=None,
             gcs_bucket=None,
             processed=False):

    curr_date = datetime.now().strftime('%Y-%m-%d')

    if processed:
        filename = f'{table}-extract-{curr_date}-processed.csv'
        state = 'processed'
    else:
        filename = f'{table}-extract-{curr_date}.csv'
        state = 'raw'

    data_folder = Variable.get('data_folder')
    data_path = f'{data_folder}/{database}/{table}'

    client = storage.Client(project=project)
    bucket = client.get_bucket(gcs_bucket)
    blob = bucket.blob(f'{state}/{database}/{table}/{filename}')
    blob.upload_from_filename(filename=f'{data_path}/{filename}')
