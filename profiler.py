# -*- coding: UTF-8 -*-

import fire
from loguru import logger

from src.backends import MongoBackend
from src.twitter import TweetsDownloader


class Profiler:
    """
    Execution:
    python src.py download_tweets --users Albert_Rivera,sanchezcastejon
    """

    def download_tweets(self, users='Pablo_Iglesias_,pablocasado_', save=True):
        try:
            t_downloader = TweetsDownloader(MongoBackend())
            for user in users:
                t_downloader.download_timeline(user, save=save)
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    fire.Fire(Profiler)
