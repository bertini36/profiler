# -*- coding: UTF-8 -*-

import time

import tweepy
from loguru import logger

from settings import (
    TWITTER_PUBLIC_KEY, TWITTER_SECRET_KEY,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)


class TweetsDownloader:

    def __init__(self, storage_backend):
        self._public_key = TWITTER_PUBLIC_KEY
        self._secret_key = TWITTER_SECRET_KEY
        self._access_token = TWITTER_ACCESS_TOKEN
        self._access_token_secret = TWITTER_ACCESS_TOKEN_SECRET
        self._storage_backend = storage_backend
        self.api = self.connect()

    @logger.catch
    def connect(self) -> tweepy.API:
        auth = tweepy.OAuthHandler(self._public_key, self._secret_key)
        auth.set_access_token(self._access_token, self._access_token_secret)
        return tweepy.API(auth)

    def save_timeline(self, timeline: dict):
        user_doc = self._storage_backend.get_timeline(timeline['user'])
        if user_doc:
            logger.info(f'Timeline already saved in {self._storage_backend}')
            self._storage_backend.delete_timeline(timeline['user'])
        self._storage_backend.save_timeline(timeline)
        self._storage_backend.disconnect()

    def download_timeline(self, username: str, limit=None, save=False) -> dict:
        """
        Download user tweets ignoring retweets
        :param username: Twitter username
        :param save: If True timeline will be saved in backend storage
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
        if save:
            self.save_timeline(timeline)
        return timeline
