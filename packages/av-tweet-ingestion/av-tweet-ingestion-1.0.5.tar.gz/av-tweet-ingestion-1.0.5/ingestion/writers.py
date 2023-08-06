import json
import logging

from tempfile import TemporaryDirectory

import os
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from ingestion.exceptions import InvalidDataTypeForIngestionException
from ingestion.logconfig import c_handler
# from ingestion.logconfig import f_handler

# Setup Logger
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
logger.addHandler(c_handler)
# logger.addHandler(f_handler)






class FileWriter:
    '''
    Class responsible for writing data to a file.
    '''

    def __init__(self, folder_name = ''):
        self._build_address(folder_name)
        self.data_dict = {'data' : []}


    def _build_address(self, folder_name):
        self.address = str(folder_name) + f'/{ datetime.strftime( datetime.now(), "%Y-%m-%d-%H_%M" ) }.json'
        logger.info(f'Preparing to write data into {self.address}')


    def write_file(self, data):
        '''
        Write data into file.
        '''
        os.makedirs(os.path.dirname(self.address), exist_ok=True)

        if isinstance(data, dict):
            self.data_dict['data'].append(data)
            with open(self.address, "a") as f:
                f.write(json.dumps(self.data_dict, indent = 6, sort_keys = True))
            logger.info(f'Tweets successfuly saved into the file.')
        
        elif isinstance(data, list):
            for element in (data):
                self.data_dict['data'].append(element)
            with open(self.address, "a") as f:
                f.write(json.dumps(self.data_dict, indent = 6, sort_keys = True))
            logger.info('Tweets successfuly saved into file.')

        else:
            raise InvalidDataTypeForIngestionException(data)





class S3Writer(FileWriter):
    '''
    Use FileWriter to write temp files and upload them to s3.
    '''

    def __init__(self, folder_name):
        super().__init__(folder_name)
        self.bucket_name = os.environ.get("S3_BUCKET_NAME")
        self.landing_layer = os.environ.get("S3_LANDING_LAYER")
        self._transform_adresses()


    def _transform_adresses(self):
        self.temp_dir = TemporaryDirectory()
        self.s3_path_key =  f"{self.landing_layer}/{self.address}"
        self.address = self.temp_dir.name + self.address
        logger.debug('Temp address: ' + self.address)
        logger.info('S3 path key: ' + self.s3_path_key)


    def write_file(self, data):
        super().write_file(data)
        
        s3_client = boto3.client('s3',
                                aws_access_key_id = os.environ.get("S3_ACESS_KEY"),
                                aws_secret_access_key = os.environ.get("S3_SECRET_KEY"))
        
        try:
            s3_client.upload_file(self.address,
                                self.bucket_name,
                                self.s3_path_key)
        except ClientError as e:
            logger.error(e)
            return False
        logger.info('File uploaded to S3 bucket.')
        self.temp_dir.cleanup()