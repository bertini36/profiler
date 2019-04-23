# -*- coding: UTF-8 -*-


from loguru import logger


class TweetsDownloader:

    def __init__(self, provider, storage_backend):
        self._provider = provider
        self._storage_backend = storage_backend

    def save_timeline(self, timeline: dict):
        user_doc = self._storage_backend.get_timeline(timeline['user'])
        if user_doc:
            logger.info(f'Timeline already saved in {self._storage_backend}')
            self._storage_backend.delete_timeline(timeline['user'])
        self._storage_backend.save_timeline(timeline)
        self._storage_backend.disconnect()

    def get_timeline(self, username: str, limit=None, save=False):
        """
        Download user tweets ignoring retweets
        :param username: Twitter username
        :param limit: Number of tweets to download
        :param save: If True timeline will be saved in backend storage
        """
        timeline = self._provider.download_timeline(username, limit)
        if save:
            self.save_timeline(timeline)
