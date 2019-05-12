# -*- coding: UTF-8 -*-

import time
from abc import ABC, abstractmethod, abstractproperty

import tweepy
from loguru import logger

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
    def download_timeline(self, username: str, limit=None):
        pass


class TweepyProvider(Provider):

    def __init__(self, public_key, secret_key, access_token, secret_token):
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
        try:
            tweet = cursor.next()
        except tweepy.TweepError:
            raise UserDoesNotExist(
                f'User {username} does not exist '
                f'or it has not registered tweets'
            )
        while True:
            try:
                if not tweet.retweeted and 'RT @' not in tweet.full_text:
                    timeline['tweets'].append({
                        'id': tweet.id,
                        'created_at': tweet.created_at,
                        'text': tweet.full_text,
                    })
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
