# -*- coding: UTF-8 -*-

import pandas as pd
from loguru import logger

from .exceptions import TimelineDoesNotExist


class Preprocessor:

    def __init__(self, storage_backend):
        self._storage_backend = storage_backend

    def process(self, username: str, save=True) -> dict:
        """
        This function gets a timeline from storage backend and
        clean text of each tweet for future procedures
        :param username: Twitter username
        :param save: If True cleaned timeline will be saved at backend storage
        """
        screen_name = f'@{username}' if '@' not in username else username
        logger.info(f'Preprocessing {screen_name} timeline')
        timeline = self._storage_backend.get_timeline(screen_name)
        if not timeline:
            raise TimelineDoesNotExist(
                f'There is no timeline for {screen_name} saved in '
                f'{self._storage_backend}. Please first, download it'
            )
        cleaned_timeline = self.clean_timeline(timeline)
        if save:
            self._storage_backend.update_timeline(screen_name, cleaned_timeline)
        return cleaned_timeline

    def clean_timeline(self, timeline: dict) -> dict:
        """
        This function will do all text
        transformations for each tweet in timeline
        """
        df = pd.DataFrame(timeline['tweets'], columns=['created_at', 'text'])
        logger.info(f'Preprocessing {df.shape[0]} tweets of {timeline["user"]}')
        # TODO: Use small textual funcions based on regex with Pandas apply
        return {
            'user': timeline['user'],
            'tweets': timeline['tweets'],
            'cleaned_tweets': list(df.T.to_dict().values())
        }
