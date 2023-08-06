import logging
from abc import ABC, abstractmethod

import requests
from backoff import expo, on_exception
from ratelimit import RateLimitException, limits
from ingestion.exceptions import QueryErrorException, AccessUnauthorizedException
from ingestion.logconfig import c_handler
# from ingestion.logconfig import f_handler


# Constants
FIFTEEN_MINUTES = 900


# Setup Logger
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
logger.addHandler(c_handler)
# logger.addHandler(f_handler)





class TweetOauth2API(ABC):
    '''
    Base class to connect to Twitter API V2 via OAuth2.
    '''
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.url = "not defined"



    def _bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    @abstractmethod
    def get_tweets(self, *args, **kargs):
        '''Implement get_tweets method'''




class RecentAPI(TweetOauth2API):
    '''
    Class to interact with Twitter's Recent API.
    '''

    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.url = "https://api.twitter.com/2/tweets/search/recent"

    
    @staticmethod
    def _check_response_errors(response):
        response_json = response.json()
        if 'errors' in response_json:
            error_msg = response_json['errors'][0]
            logger.error(error_msg)
            raise QueryErrorException(error_msg)
        if response.status_code == 401:
            logger.error(AccessUnauthorizedException(response.status_code))
            raise AccessUnauthorizedException(response.status_code)

    # "App rate limit (OAuth 2.0 App Access Token): 450 requests per 15-minute window shared among all users of your app"
    @on_exception(expo, RateLimitException, max_tries=5)
    @limits(calls=100, period=FIFTEEN_MINUTES)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=5)
    def get_tweets(self,
                    query_params,
                    n_requests = 2):
        '''
        Params:
            query_params = [dict] Query and filds to request the API, please see Twitter's API Documentation for more info.
            n_requests =  [int] Number of hits at the API to pull tweets.
        
        '''
        next_token_flag = False
        responses = []
        for i in range(n_requests):
            if not next_token_flag:
                next_token_flag = True
                response = requests.get(self.url, auth=super()._bearer_oauth, params=query_params)
                RecentAPI._check_response_errors(response)
                logger.info(f'First request response; {response.status_code}')
                responses.append(response.json())
            else:
                query_params['next_token'] = response.json()['meta']['next_token']
                response = requests.get(self.url, auth=super()._bearer_oauth, params=query_params)
                logger.debug(f'{i+1}st request response; {response.status_code}')
                responses.append(response.json())
        
        return responses
