""" Read data from local file, API endpoint, GCP, or AWS """

from os import environ
import pandas as pd

# api calls
import requests
import backoff

# GCP
import google.auth
from google.cloud import storage, bigquery

# AWS
import boto3


def read_local_csv(path):
    """
    Read local csv file into a dataframe
    https://pandas.pydata.org/pandas-docs/stable/io.html#io-read-csv-table
    """
    df = pd.read_csv('.csv')
    return df

#--------------#
# API endpoint #
#--------------#
@backoff.on_exception(backoff.constant, (requests.exceptions.RequestException),
                      jitter=backoff.random_jitter, max_tries=5, interval=30)
def send_get_request_to_api(url):
    """
    Send get request to API endpoint
    http://docs.python-requests.org/en/master/
    https://pypi.org/project/backoff/
    """
    response = session.get(url=url)
    response.raise_for_status()
    return response

#----------------------#
# Google Cloud Storage #
#----------------------#
def download_file_from_gcs(bucket_name, remote_path, local_path):
    """
    Download a file from Google Cloud Storage
    http://google-cloud-python.readthedocs.io/en/latest/storage/buckets.html
    """
    CREDENTIALS, _ = google.auth.default()
    GCS_BUCKET = storage.Client().get_bucket(bucket_name)
    GCS_BUCKET.get_blob(remote_path).download_to_filename(local_path)
    return

#-----------------#
# Google BigQuery #
#-----------------#
def query_bq_table(query_str):
    """
    Query a table in BigQuery
    http://google-cloud-python.readthedocs.io/en/latest/bigquery/usage.html

    Example query:
    query_str = ('SELECT p.ticker AS ticker, '
                 'p.date AS date, '
                 'p.price AS price, '
                 's.name AS name '
                 'FROM `stocks.price_daily` p '
                 'LEFT OUTER JOIN `stocks.symbol` s '
                 'ON p.ticker = s.ticker ')
    """
    client = bigquery.Client()
    df = client.query(query_str).to_dataframe()
    return

#--------#
# AWS S3 #
#--------#
def download_file_from_s3(bucket_name, remote_path, local_path):
    """
    Download a file from AWS S3
    http://boto3.readthedocs.io/en/latest/guide/s3-examples.html
    """
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(remote_path, local_path)
    return
