# -*- coding: UTF-8 -*-

from loguru import logger


class TimelineDownloader:

    def __init__(self, provider, storage_backend):
        self._provider = provider
        self._storage_backend = storage_backend

    def save_timeline(self, timeline: dict):
        user = timeline['user']
        with self._storage_backend as backend:
            if backend.exists_timeline(user):
                logger.info(
                    f'Timeline already saved in {backend}'
                )
                backend.update_timeline(user, timeline)
            else:
                backend.insert_timeline(timeline)

    def get_timeline(
        self, username: str, limit: int = None, save: bool = False
    ):
        """
        Download user tweets ignoring retweets
        :param username: Twitter username
        :param limit: Number of tweets to download
        :param save: If True timeline will be saved in backend storage
        """
        logger.info(f'Downloading tweets using {self._provider}')
        with self._provider as provider:
            timeline = provider.download_timeline(username, limit)
            if save:
                self.save_timeline(timeline)