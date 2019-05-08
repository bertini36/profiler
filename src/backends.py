# -*- coding: UTF-8 -*-

from abc import ABC, abstractmethod, abstractproperty

import pymongo
from loguru import logger

from .exceptions import DatabaseDoesNotExist


class Backend(ABC):

    def __repr__(self):
        return self.name

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractmethod
    def insert_timeline(self, timeline: dict):
        pass

    @abstractmethod
    def get_timeline(self, user: str):
        pass

    @abstractmethod
    def update_timeline(self, user: str, new_values):
        pass

    @abstractmethod
    def delete_timeline(self, user: str):
        pass

    def exists_timeline(self, user: str) -> bool:
        if self.get_timeline(user):
            return True
        return False


class MongoBackend(Backend):

    def __init__(self, mongo_url, mongo_port, db_name, use_existing_db=True):
        self.url = mongo_url
        self.port = mongo_port
        self.db_name = db_name
        self.use_existing_db = use_existing_db
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
        if self.db_name in self.client.list_database_names():
            if self.use_existing_db:
                logger.info('Database already exists and it will be used')
            else:
                raise DatabaseDoesNotExist(
                    'Database already exists, set USE_EXISTING'
                    '_DATABASE=True if you want to use it'
                )
        else:
            logger.info('Database doesn\'t exist, it will be created')
        return self.client[self.db_name]

    @property
    def timeline_collection(self):
        return self.db.timelines

    def insert_timeline(self, timeline: dict):
        logger.info(f'Inserting {len(timeline["tweets"])} tweets with {self}')
        self.timeline_collection.insert_one(timeline)

    def get_timeline(self, user: str) -> dict:
        return self.timeline_collection.find_one({'user': user})

    def update_timeline(self, user: str, new_values):
        logger.info(f'Updating {user} timeline')
        query = {'user': user}
        self.timeline_collection.update_one(query, {'$set': new_values})

    def delete_timeline(self, user: str):
        logger.info(f'Deleting {user} timeline')
        self.timeline_collection.remove({'user': user})
