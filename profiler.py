# -*- coding: UTF-8 -*-

import multiprocessing as mp

import fire
from loguru import logger

from settings import (
    MONGO_URL, MONGO_PORT, MONGO_DB, USE_EXISTING_DATABASE,
    TWITTER_PUBLIC_KEY, TWITTER_SECRET_KEY,
    TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN,
    LDA_N_PASSES, LDA_USE_BIGRAMS, LDA_MIN_DF, LDA_THRESHOLD, LDA_UNANIMITY,
)
from src.backends import MongoBackend
from src.preprocessing import Preprocessor
from src.providers import TweepyProvider
from src.timeline_downloader import TimelineDownloader
from src.lda import LDA


class Profiler:

    @staticmethod
    def get_timelines(users: str = 'vidamoderna,', save: bool = True):
        """
        Exec:
        python profiler.py get_timelines --users vidamoderna,
        """
        try:
            t_downloader = TimelineDownloader(
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

    @staticmethod
    def clean_timelines(users: str = 'vidamoderna,', save: bool = True):
        """
        Exec:
        python profiler.py clean_timelines --users vidamoderna,
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
                    target=preprocessor.run,
                    args=(user,),
                    kwargs={'save': save},
                ).start()
        except Exception as e:
            logger.error(e)

    @staticmethod
    def find_topics(
        users: str = 'vidamoderna,', n_topics: int = 7, save: bool = True
    ):
        """
        Exec:
        python profiler.py find_topics --users vidamoderna,
        """
        try:
            lda = LDA(
                MongoBackend(
                    MONGO_URL,
                    MONGO_PORT,
                    MONGO_DB,
                    USE_EXISTING_DATABASE
                ),
                n_topics=n_topics,
                n_passes=LDA_N_PASSES,
                use_bigrams=LDA_USE_BIGRAMS,
                min_df=LDA_MIN_DF,
                threshold=LDA_THRESHOLD,
                unanimity=LDA_UNANIMITY
            )
            for user in users:
                mp.Process(
                    target=lda.run,
                    args=(user,),
                    kwargs={'save': save},
                ).start()
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    fire.Fire(Profiler)
