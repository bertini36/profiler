# -*- coding: UTF-8 -*-

import multiprocessing as mp

import fire
from loguru import logger

from settings import (
    MONGO_URL, MONGO_PORT, MONGO_DB, USE_EXISTING_DATABASE,
    TWITTER_PUBLIC_KEY, TWITTER_SECRET_KEY,
    TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN
)
from src.backends import MongoBackend
from src.preprocessing import Preprocessor
from src.providers import TweepyProvider
from src.tweets_downloader import TweetsDownloader


class Profiler:

    def get_timelines(self, users='Pablo_Iglesias_,pablocasado_', save=True):
        """
        Exec:
        python profiler.py get_timelines --users Albert_Rivera,sanchezcastejon
        """
        try:
            t_downloader = TweetsDownloader(
                TweepyProvider(
                    TWITTER_PUBLIC_KEY,
                    TWITTER_SECRET_KEY,
                    TWITTER_ACCESS_TOKEN,
                    TWITTER_SECRET_TOKEN
                ),
                MongoBackend(
                    MONGO_URL,
                    MONGO_PORT,
                    MONGO_DB,
                    USE_EXISTING_DATABASE
                )
            )
            for user in users:
                mp.Process(
                    target=t_downloader.get_timeline,
                    args=(user,),
                    kwargs={'save': save},
                ).start()
        except Exception as e:
            logger.error(e)

    def clean_timelines(self, users='Pablo_Iglesias_,pablocasado_', save=True):
        """
        Exec:
        python profiler.py clean_timelines --users Albert_Rivera,sanchezcastejon
        """
        try:
            preprocessor = Preprocessor(
                MongoBackend(
                    MONGO_URL,
                    MONGO_PORT,
                    MONGO_DB,
                    USE_EXISTING_DATABASE
                )
            )
            for user in users:
                mp.Process(
                    target=preprocessor.process,
                    args=(user,),
                    kwargs={'save': save},
                ).start()
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    fire.Fire(Profiler)
