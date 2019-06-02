# -*- coding: UTF-8 -*-

import pytest

from settings import (TWITTER_ACCESS_TOKEN, TWITTER_PUBLIC_KEY,
                      TWITTER_SECRET_KEY, TWITTER_SECRET_TOKEN)
from src.providers import TweepyProvider


class Tweet:

    def __init__(
        self, retweeted: bool, full_text: str,
        id: str = '', created_at: str = ''
    ):
        self.retweeted = retweeted
        self.full_text = full_text
        self.id = id
        self.created_at = created_at


@pytest.mark.unit
class TestTweepyProvider:

    @classmethod
    def setup_class(cls):
        cls.provider = TweepyProvider(
            TWITTER_PUBLIC_KEY,
            TWITTER_SECRET_KEY,
            TWITTER_ACCESS_TOKEN,
            TWITTER_SECRET_TOKEN
        )
        cls.provider.__enter__()

    def test_is_retweet(self):
        tweet = Tweet(True, 'Ouh mama')
        result = self.provider.is_retweet(tweet)
        assert result is True

    def test_is_retweet2(self):
        tweet = Tweet(False, 'RT @: Ouh mama')
        result = self.provider.is_retweet(tweet)
        assert result is True

    def test_is_not_retweet(self):
        tweet = Tweet(False, 'Ouh mama')
        result = self.provider.is_retweet(tweet)
        assert result is False
