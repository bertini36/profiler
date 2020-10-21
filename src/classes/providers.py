# -*- coding: UTF-8 -*-

import time
from abc import ABC, abstractmethod, abstractproperty

import tweepy
from loguru import logger

from .decorators import timeit
from .exceptions import UserDoesNotExist


class Provider(ABC):
    def __repr__(self):
        return self.name

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def download_timeline(
        self, user: str, limit=None, filter_retweets: bool = True
    ) -> dict:
        pass


class TweepyProvider(Provider):
    def __init__(
        self,
        public_key: str,
        secret_key: str,
        access_token: str,
        secret_token: str,
    ):
        self._public_key = public_key
        self._secret_key = secret_key
        self._access_token = access_token
        self._access_token_secret = secret_token

    @property
    def name(self):
        return 'Tweepy provider'

    @logger.catch
    def __enter__(self):
        auth = tweepy.OAuthHandler(self._public_key, self._secret_key)
        auth.set_access_token(self._access_token, self._access_token_secret)
        self.api = tweepy.API(auth)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def is_retweet(tweet):
        return tweet.retweeted or 'RT @' in tweet.full_text

    @timeit
    def download_timeline(
        self, user: str, limit: int = None, filter_rts: bool = False
    ) -> dict:
        """
        Download user tweets ignoring retweets
        :param user: Twitter username
        :param limit: Number of tweets to download
        :param filter_rts: Filter user retweets
        """
        logger.info(f'Downloading {user} timeline')
        timeline = {'user': user, 'tweets': []}
        cursor = tweepy.Cursor(
            self.api.user_timeline, screen_name=user, tweet_mode='extended'
        ).items()
        try:
            tweet = cursor.next()
        except tweepy.TweepError as e:
            print(e)
            raise UserDoesNotExist(
                f'User {user} does not exist '
                f'or it has not registered tweets. e: {e}'
            )
        while True:
            try:
                if filter_rts and self.__class__.is_retweet(tweet):
                    continue
                timeline['tweets'].append(
                    {
                        'id': tweet.id,
                        'created_at': tweet.created_at,
                        'text': tweet.full_text,
                    }
                )
                if limit and len(timeline['tweets']) >= limit:
                    break
                tweet = cursor.next()
            except tweepy.TweepError:
                logger.warning('TweepError: Delaying...')
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        return timeline
