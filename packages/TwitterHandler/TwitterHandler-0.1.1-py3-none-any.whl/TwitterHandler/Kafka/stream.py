import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from tweepy import StreamingClient, StreamRule
from tweepy.asynchronous import AsyncStreamingClient, AsyncClient
from kafka import KafkaProducer
import asyncio
import aiohttp
import tweepy

bearer_token = os.environ['BEARER_TOKEN']


class TweetsStreamer(StreamingClient):
    def __init__(self, producer, **kwargs):
        super().__init__(**kwargs)
        self.producer = producer

    def on_data(self, raw_data):
        try:
            self.producer.send(
                'tweets_stream', raw_data)
        except BaseException as e:
            print(e)
        return True

    def on_error(self, status_code):
        print(status_code)



class AsyncTweetsStreamer(AsyncStreamingClient):
    def __init__(self, producer, **kwargs):
        super().__init__(**kwargs)
        self.producer = producer

    async def on_data(self, raw_data):
        try:
            self.producer.send(
                'tweets_stream', raw_data)
        except BaseException as e:
            print(e)
        return True

    async def on_error(self, status_code):
        print(status_code)


class AsyncTweets:
    def __init__(self,):
        self.async_client = AsyncClient(bearer_token=bearer_token)

    def get_recent_tweets_count(self, query):
        tweets = self.async_client.get_recent_tweets_count(query=query)
        return tweets

    
class Streamer:
    def __init__(self, ):
        producer = KafkaProducer(bootstrap_servers="localhost:9092")
        self.streamer = TweetsStreamer(producer, bearer_token=bearer_token)

    def start_stream(self, query):
        self.streamer.add_rules(StreamRule(query))
        self.streamer.filter(threaded=True, )


if __name__ == '__main__':
    # producer = KafkaProducer(bootstrap_servers="localhost:9092")
    # streamer = TweetsStreamer(producer, bearer_token=bearer_token)
    # streamer.add_rules(StreamRule("Trump"))
    # streamer.filter(threaded=True)
    # print('Streaming tweets...')

    # at = AsyncTweets()
    # res = at.get_recent_tweets_count('Trump')
    # asyncio.run(res)
    # print('Streaming tweets...')
    # print(res)
    streamer= Streamer()
    streamer.start_stream('Trump')
    print('Streaming tweets...')

