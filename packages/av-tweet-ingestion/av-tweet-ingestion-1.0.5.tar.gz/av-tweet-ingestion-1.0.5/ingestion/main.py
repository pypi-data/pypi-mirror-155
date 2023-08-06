import logging

from dotenv import load_dotenv
from logconfig import c_handler
from logconfig import f_handler

from apis import RecentAPI
from ingestors import BatchIngestor
from writers import FileWriter, S3Writer

if __name__ == "__main__": # pragma: no cover

    # Setup Logger
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')
    logger.addHandler(c_handler)
    # logger.addHandler(f_handler)




    load_dotenv()


    # Define QUERY
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    # query_params = {
    #                 'query': '"World Cup"',
    #                 'user.fields':'id,location,name,public_metrics',
    #                 'tweet.fields': 'author_id,public_metrics',
    #                 'expansions':'geo.place_id,author_id,entities.mentions.username,in_reply_to_user_id,referenced_tweets.id.author_id',
    #                 'max_results':'100'
    #                 }
    query_params = {
                    'query': 'from: elonmusk',
                    'user.fields':'id,location,name,public_metrics,created_at',
                    'tweet.fields': 'author_id',
                    # 'expansions':'geo.place_id,author_id,entities.mentions.username,in_reply_to_user_id,referenced_tweets.id.author_id',
                    'max_results':'10'
                    }


    BatchIngestor(query_params,
                1,
                RecentAPI,
                'test/RecentAPI',
                FileWriter).ingest()

