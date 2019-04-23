# -*- coding: UTF-8 -*-

import time
from abc import ABC, abstractmethod, abstractproperty

import tweepy
from loguru import logger


class Provider(ABC):

    def __repr__(self):
        return self.name

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def download_timeline(self, username: str, limit=None):
        pass


class TweepyProvider(Provider):

    def __init__(self, public_key, secret_key, access_token, secret_token):
        self._public_key = public_key
        self._secret_key = secret_key
        self._access_token = access_token
        self._access_token_secret = secret_token
        self.api = self.connect()

    @property
    def name(self):
        return 'Tweepy provider'

    @logger.catch
    def connect(self) -> tweepy.API:
        auth = tweepy.OAuthHandler(self._public_key, self._secret_key)
        auth.set_access_token(self._access_token, self._access_token_secret)
        return tweepy.API(auth)

    def download_timeline(self, username: str, limit=None) -> dict:
        """
        Download user tweets ignoring retweets
        :param username: Twitter username
        :param limit: Number of tweets to download
        """
        screen_name = f'@{username}' if '@' not in username else username
        logger.info(f'Downloading {screen_name} timeline')
        timeline = {'user': screen_name, 'tweets': []}
        cursor = tweepy.Cursor(
            self.api.user_timeline,
            screen_name=screen_name,
            tweet_mode='extended'
        ).items()
        while True:
            try:
                tweet = cursor.next()
                if not tweet.retweeted and 'RT @' not in tweet.full_text:
                    timeline['tweets'].append({
                        'created_at': tweet.created_at,
                        'text': tweet.full_text,
                    })
                    if limit and len(timeline['tweets']) >= limit:
                        break
            except tweepy.TweepError:
                logger.warning('TweepError: Delaying...')
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        return timeline
