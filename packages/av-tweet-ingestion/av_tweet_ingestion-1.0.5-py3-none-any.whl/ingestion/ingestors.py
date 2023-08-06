import os
import logging
from dotenv import load_dotenv
from ingestion.logconfig import c_handler
# from ingestion.logconfig import f_handler

# Setup Logger
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
logger.addHandler(c_handler)
# logger.addHandler(f_handler)

class BatchIngestor:
    '''
    Represents a base class for ingestor.

    Params:
        bearer_token = [str] Twitter's BearerToken.
        query_params = [dict] Query and filds to request the API, please see Twitter's API Documentation for more info. 
        n_requests = [int] Number of hits at the API to pull tweets.
        api_cls = [subclass of TweetOauth2API] API Object to pull tweets.
        writers_cls = [class FileWriter or list of FileWriter] Class responsible for writing data permanently, more than one writer can be used.
        folder_name = [str] Optional. Folder name, usually API's name.
    '''

    def __init__(self, query_params, n_requests, api_cls, folder_name, writers_cls):
        if os.getenv('ENVIRONMENT') == "local":
            load_dotenv()
        self.api_cls = api_cls
        self.bearer_token = os.environ.get("BEARER_TOKEN")
        self.query_params = query_params
        self.n_requests = n_requests
        self.folder_name = folder_name
        if not isinstance(writers_cls, list):
            self.writers_cls = [writers_cls]
        else:
            self.writers_cls = writers_cls
            logger.debug("List of writers ",self.writers_cls)    
        

    def _get_data(self):
        return self.api_cls(self.bearer_token).get_tweets(self.query_params, self.n_requests)

    def ingest(self):
        data = self._get_data()
        for writer in self.writers_cls:
            writer(self.folder_name).write_file(data)