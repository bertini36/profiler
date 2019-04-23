# -*- coding: UTF-8 -*-

import multiprocessing as mp

import fire
from loguru import logger

from src.backends import MongoBackend
from src.providers import TweepyProvider
from src.tweets_downloader import TweetsDownloader
from settings import (
    TWITTER_PUBLIC_KEY, TWITTER_SECRET_KEY,
    TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN
)


class Profiler:
    """
    Execution:
    python profiler.py get_timelines --users Albert_Rivera,sanchezcastejon
    """

    def get_timelines(self, users='Pablo_Iglesias_,pablocasado_', save=True):
        try:
            t_downloader = TweetsDownloader(
                TweepyProvider(
                    TWITTER_PUBLIC_KEY,
                    TWITTER_SECRET_KEY,
                    TWITTER_ACCESS_TOKEN,
                    TWITTER_SECRET_TOKEN
                ),
                MongoBackend()
            )
            for user in users:
                mp.Process(
                    target=t_downloader.get_timeline,
                    args=(user,),
                    kwargs={'save': save},
                ).start()
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    fire.Fire(Profiler)
