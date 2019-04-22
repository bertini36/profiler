# -*- coding: UTF-8 -*-

import multiprocessing as mp

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
            processes = [
                mp.Process(
                    target=t_downloader.download_timeline,
                    args=(user,),
                    kwargs={'save': save},
                ) for user in users
            ]
            for p in processes:
                p.start()
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    fire.Fire(Profiler)
