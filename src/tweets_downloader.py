# -*- coding: UTF-8 -*-

from loguru import logger


class TweetsDownloader:

    def __init__(self, provider, storage_backend):
        self._provider = provider
        self._storage_backend = storage_backend

    def save_timeline(self, timeline: dict):
        user = timeline['user']
        if self._storage_backend.exists_timeline(user):
            logger.info(
                f'Timeline already saved in {self._storage_backend}'
            )
            self._storage_backend.update_timeline(user, timeline)
        self._storage_backend.insert_timeline(timeline)
        self._storage_backend.disconnect()

    def get_timeline(self, username: str, limit=None, save=False):
        """
        Download user tweets ignoring retweets
        :param username: Twitter username
        :param limit: Number of tweets to download
        :param save: If True timeline will be saved in backend storage
        """
        logger.info(f'Downloading tweets using {self._provider}')
        timeline = self._provider.download_timeline(username, limit)
        if save:
            self.save_timeline(timeline)
