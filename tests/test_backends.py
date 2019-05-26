# -*- coding: UTF-8 -*-

import pymongo
import pytest
from mock import patch

from settings import MONGO_URL, MONGO_PORT, MONGO_DB, USE_EXISTING_DATABASE
from src.backends import MongoBackend
from src.exceptions import DatabaseDoesNotExist


@pytest.mark.unit
class TestMongoBackend:

    @classmethod
    def setup_class(cls):
        cls.backend = MongoBackend(
            MONGO_URL,
            MONGO_PORT,
            MONGO_DB,
            USE_EXISTING_DATABASE
        )
        cls.backend.client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)

    @patch('pymongo.MongoClient.list_database_names')
    @patch('loguru.logger.info')
    def test_get_db_that_exists(self, logger_mock, list_dbs_mock):
        self.backend.use_existing_db = True
        list_dbs_mock.return_value = [MONGO_DB]
        self.backend.get_db()
        logger_mock.assert_called_with(
            'Database already exists and it will be used'
        )

    @patch('pymongo.MongoClient.list_database_names')
    def test_get_db_that_exists_but_not_use_existing_db(self, list_dbs_mock):
        self.backend.use_existing_db = False
        list_dbs_mock.return_value = [MONGO_DB]
        with pytest.raises(DatabaseDoesNotExist):
            self.backend.get_db()

    @patch('pymongo.MongoClient.list_database_names')
    @patch('loguru.logger.info')
    def test_get_db_that_does_not_exist(self, logger_mock, list_dbs_mock):
        list_dbs_mock.return_value = []
        self.backend.get_db()
        logger_mock.assert_called_with(
            'Database doesn\'t exist, it will be created'
        )
