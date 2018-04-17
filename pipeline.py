from os import environ
from datetime import datetime, timedelta
import logging

# py-project modules
from load import read_local_csv, send_get_request_to_api, \
                 download_file_from_gcs, download_file_from_s3
from clean import convert_column_to_datetime

# luigi
import luigi
from luigi.contrib import gcs as luigi_gcs
from luigi.contrib import external_program


#-------#
# Dates #
#-------#
TODAY = datetime.today()
YESTERDAY = TODAY - timedelta(days=1)

#----------------------#
# Google Cloud Storage #
#----------------------#
PROJECT_ID = 'my-project'
BUCKET_NAME = 'my-bucket'
BUCKET_PATH = 'gs://{}'.format(BUCKET_NAME)
GCS_CLIENT = luigi_gcs.GCSClient(CREDENTIALS)

#---------#
# Logging #
#---------#
logger = logging.getLogger('luigi-interface')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('logs/{date:%Y-%m-%d}-luigi.log'.format(date=YESTERDAY))
fh.setLevel(logging.INFO)
logger.addHandler(fh)


class LoadData(luigi.Task):
    """Load data from remote host (API, S3, GCS) and save to local csv"""
    date = luigi.DateParameter()

    def requires(self):
        return []

    def output(self):
        output_path_template = '{}/{date:%Y-%m-%d}.csv'
        # output_path = output_path_template.format(BUCKET_PATH, date=self.date)
        # return luigi_gcs.GCSTarget(output_path, client=GCS_CLIENT)
        output_path = output_path_template.format('data', date=self.date)
        return luigi.LocalTarget(output_path)

    def run(self):
        with self.output().open('w') as out_file:
            df.to_csv(out_file, index=False)
        return


class CleanData(luigi.Task):
    """Clean data"""
    date = luigi.DateParameter()

    def requires(self):
        return LoadData(self.date)

    def output(self):
        output_path_template = '{}/{date:%Y-%m-%d}.csv'
        output_path = output_path_template.format(BUCKET_PATH, date=self.date)
        return luigi.LocalTarget(output_path)

    def run(self):
        with self.input().open('r') as in_file:
            df = pd.read_csv(in_file)
        with self.output().open('w') as out_file:
            df.to_csv(out_file, index=False)
        return


class GenerateReport(luigi.Task):
    date = luigi.DateParameter()

    def requires(self):
        return CleanData(self.date)

    def output(self):
        output_path_template = '{}/{date:%Y-%m-%d}.txt'
        output_path = output_path_template.format('report', date=self.date)
        return luigi.LocalTarget(output_path)

    def run(self):
        with self.input().open('r') as in_file:
            df = pd.read_csv(in_file)
        with self.output().open('w') as out_file:
            out_file.write('done')
        return


class RunExternal(external_program.ExternalProgramTask):
    def requires(self):
        return []

    def program_args(self):
        return ['./script.sh']


if __name__ == '__main__':
    luigi.run()
