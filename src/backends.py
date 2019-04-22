# -*- coding: UTF-8 -*-

from abc import ABC, abstractmethod, abstractproperty

import pymongo
from loguru import logger

from .exceptions import DatabaseDoesNotExist
from settings import MONGO_URL, MONGO_PORT, MONGO_DB, USE_EXISTING_DATABASE


class Backend(ABC):

    def __repr__(self):
        return self.name

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractmethod
    def save_timeline(self, timeline: dict):
        pass

    @abstractmethod
    def get_timeline(self, user: str):
        pass

    @abstractmethod
    def delete_timeline(self, user: str):
        pass


class MongoBackend(Backend):

    def __init__(self):
        self.url = MONGO_URL
        self.port = MONGO_PORT
        self.client = self.connect()
        self.db = self.get_db()

    @property
    def name(self):
        return 'Mongo backend'

    @logger.catch
    def connect(self):
        return pymongo.MongoClient(self.url, self.port)

    @logger.catch
    def disconnect(self):
        self.client.close()

    def get_db(self):
        if MONGO_DB in self.client.list_database_names():
            if USE_EXISTING_DATABASE:
                logger.info('Database already exists and it will be used')
            else:
                logger.warning(
                    'Database already exists, set '
                    'USE_EXISTING_DATABASE=True if you want to use it'
                )
                raise DatabaseDoesNotExist()
        else:
            logger.info('Database doesn\'t exist, it will be created')
        return self.client[MONGO_DB]

    @property
    def timeline_collection(self):
        return self.db.timelines

    def save_timeline(self, timeline: dict):
        logger.info(f'Saving {len(timeline["tweets"])} tweets with {self}')
        return self.timeline_collection.insert_one(timeline).inserted_id

    def get_timeline(self, user: str) -> dict:
        return self.timeline_collection.find_one({'user': user})

    def delete_timeline(self, user: str):
        logger.info(f'Deleting {user} timeline')
        self.timeline_collection.remove({'user': user})
