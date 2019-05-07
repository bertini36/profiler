# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np

from loguru import logger

from .exceptions import TimelineDoesNotExist


class Preprocesser:

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
                f'There is no timeline for {screen_name}'
                f' saved in {self._storage_backend}'
            )
        cleaned_timeline = self.clean_timeline(timeline)
        if save:
            self._storage_backend.save_timeline(cleaned_timeline)
        return cleaned_timeline

    def clean_timeline(self, timeline: dict) -> dict:
        """
        This function will do all text
        transformations for each tweet in timeline
        TODO: timeline['tweets'] -> Pandas data frame
              Use small textual funcion based on regex with Pandas apply
              Create new data frame column with clened_tweets
              Return new timeline structure: {'user': '', 'tweets': [], 'cleaned_tweets': []}
        """
        pass
