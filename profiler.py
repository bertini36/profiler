# -*- coding: UTF-8 -*-

import multiprocessing as mp

import fire
from loguru import logger

from settings import (
    MONGO_URL, MONGO_PORT, MONGO_DB, USE_EXISTING_DATABASE, TWITTER_PUBLIC_KEY,
    TWITTER_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN,
    REPLACE_MENTIONS, FILTER_MENTIONS, REPLACE_EMAILS, FILTER_EMAILS,
    REPLACE_CURRENCIES, FILTER_CURRENCIES, REPLACE_URLS, FILTER_URLS,
    REPLACE_PHONE_NUMBERS, FILTER_PHONE_NUMBERS, REPLACE_NUMBERS,
    FILTER_NUMBERS, REPLACE_DIGITS, FILTER_DIGITS, REPLACE_EMOJIS,
    FILTER_EMOJIS, REMOVE_PUNCT, REMOVE_MULTIPLE_SPACES, TO_LOWER,
    FILTER_STOPWORDS, FILTER_EMPTY_ROWS, LDA_N_PASSES, LDA_USE_BIGRAMS,
    LDA_MIN_DF, FILTER_RTS
)
from src.backends import MongoBackend
from src.preprocessors import MyPreprocessor
from src.providers import TweepyProvider
from src.timeline_downloader import TimelineDownloader
from src.lda import LDA


class Profiler:

    @staticmethod
    def clean_user(user):
        return f'@{user}' if '@' not in user else user

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
            pool = []
            for user in users:
                process = mp.Process(
                    target=t_downloader.get_timeline,
                    args=(Profiler.clean_user(user),),
                    kwargs={'save': save, 'filter_rts': FILTER_RTS},
                )
                process.start()
                pool.append(process)
            for process in pool:
                process.join()
        except Exception as e:
            logger.error(e)

    @staticmethod
    def clean_timelines(users: str = 'vidamoderna,', save: bool = True):
        """
        Exec:
        python profiler.py clean_timelines --users vidamoderna,
        """
        try:
            preprocessor = MyPreprocessor(
                MongoBackend(
                    MONGO_URL,
                    MONGO_PORT,
                    MONGO_DB,
                    USE_EXISTING_DATABASE
                ),
            )
            pool = []
            for user in users:
                process = mp.Process(
                    target=preprocessor.run,
                    args=(Profiler.clean_user(user),),
                    kwargs={
                        'save': save,
                        'replace_mentions': REPLACE_MENTIONS,
                        'filter_mentions': FILTER_MENTIONS,
                        'replace_emails': REPLACE_EMAILS,
                        'filter_emails': FILTER_EMAILS,
                        'replace_currencies': REPLACE_CURRENCIES,
                        'filter_currencies': FILTER_CURRENCIES,
                        'replace_urls': REPLACE_URLS,
                        'filter_urls': FILTER_URLS,
                        'replace_numbers': REPLACE_NUMBERS,
                        'filter_numbers': FILTER_NUMBERS,
                        'replace_digits': REPLACE_DIGITS,
                        'filter_digits': FILTER_DIGITS,
                        'replace_emojis': REPLACE_EMOJIS,
                        'filter_emojis': FILTER_EMOJIS,
                        'remove_punct': REMOVE_PUNCT,
                        'remove_multiple_spaces': REMOVE_MULTIPLE_SPACES,
                        'to_lower': TO_LOWER,
                        'filter_stopwords': FILTER_STOPWORDS,
                        'filter_empty_rows': FILTER_EMPTY_ROWS
                    },
                )
                process.start()
                pool.append(process)
            for process in pool:
                process.join()
        except Exception as e:
            logger.error(e)

    @staticmethod
    def find_topics(
        users: str = 'vidamoderna,', save: bool = True, n_topics: int = 5
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
                min_df=LDA_MIN_DF
            )
            pool = []
            for user in users:
                process = mp.Process(
                    target=lda.run,
                    args=(Profiler.clean_user(user),),
                    kwargs={'save': save},
                )
                process.start()
                pool.append(process)
            for process in pool:
                process.join()
        except Exception as e:
            logger.error(e)

    @staticmethod
    def run_all(
        users: str = 'vidamoderna,', save: bool = True,  n_topics: int = 5
    ):
        Profiler.get_timelines(users, save)
        Profiler.clean_timelines(users, save)
        Profiler.find_topics(users, save, n_topics)


if __name__ == '__main__':
    fire.Fire(Profiler)
