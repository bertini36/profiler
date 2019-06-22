# -*- coding: UTF-8 -*-

import pytest
from mock import patch

from src.classes.backends import MongoBackend
from src.classes.exceptions import TimelineDoesNotExist
from src.classes.lda import LDA
from src.settings import MONGO_DB, MONGO_PORT, MONGO_URL, USE_EXISTING_DATABASE


@pytest.mark.unit
class TestLDA:

    @classmethod
    def setup_class(cls):
        cls.backend = MongoBackend(
            MONGO_URL,
            MONGO_PORT,
            MONGO_DB,
            USE_EXISTING_DATABASE
        )
        cls.lda = LDA(cls.backend)
        cls.timeline = {
            'user': '@test',
            'tweets': [
                {
                    'id': 1,
                    'created_at': '',
                    'text': 'Ouh mama'
                },
                {
                    'id': 2,
                    'created_at': '',
                    'text': 'Ey yo'
                }
            ],
            'cleaned_tweets': [
                {
                    'id': 1,
                    'created_at': '',
                    'text': 'ouh mama'
                },
                {
                    'id': 2,
                    'created_at': '',
                    'text': 'ey yo'
                }
            ],
            'models': {
                '111': None
            }
        }

    @patch('src.classes.backends.MongoBackend.get_timeline')
    def test_get_timeline(self, get_timeline_mock):
        get_timeline_mock.return_value = 1
        result = self.lda.get_timeline('@test', self.backend)
        assert result == 1

    @patch('src.classes.backends.MongoBackend.get_timeline')
    def test_get_timeline(self, get_timeline_mock):
        get_timeline_mock.return_value = 0
        with pytest.raises(TimelineDoesNotExist):
            self.lda.get_timeline('@test', self.backend)

    @patch('src.classes.lda.LDA.generate_html')
    @patch('pickle.loads')
    @patch('loguru.logger.info')
    @patch('src.classes.lda.LDA.prepare_data')
    @patch('src.classes.lda.LDA.model_is_already_inferred')
    def test_infer_model_already_inferred(
        self, already_inferred_mock, prepare_data_mock,
        logger_mock, pickle_mock, generate_html_mock
    ):
        prepare_data_mock.return_value = None, None
        already_inferred_mock.return_value = True
        pickle_mock.return_value = 'model'
        model = self.lda.infer_model(self.timeline, '111')
        logger_mock.called_with('Model is already inferred')
        assert model == 'model'
        generate_html_mock.assert_called_once()

    @patch('src.classes.lda.LDA.print_terms')
    @patch('src.classes.lda.LDA.generate_html')
    @patch('pickle.loads')
    @patch('loguru.logger.info')
    @patch('src.classes.lda.LDA.prepare_data')
    @patch('src.classes.lda.LDA.model_is_already_inferred')
    def test_infer_model_already_inferred_verbose(
        self, already_inferred_mock, prepare_data_mock,
        logger_mock, pickle_mock, generate_html_mock, print_terms_mock
    ):
        prepare_data_mock.return_value = None, None
        already_inferred_mock.return_value = True
        pickle_mock.return_value = 'model'
        model = self.lda.infer_model(self.timeline, '111', verbose=True)
        logger_mock.called_with('Model is already inferred')
        assert model == 'model'
        generate_html_mock.assert_called_once()
        print_terms_mock.assert_called_once()

    @patch('gensim.models.ldamulticore.LdaMulticore.__init__')
    @patch('src.classes.lda.LDA.print_terms')
    @patch('src.classes.lda.LDA.generate_html')
    @patch('loguru.logger.info')
    @patch('src.classes.lda.LDA.prepare_data')
    @patch('src.classes.lda.LDA.model_is_already_inferred')
    def test_infer_model(
        self, already_inferred_mock, prepare_data_mock, logger_mock,
        generate_html_mock, print_terms_mock, lda_mock
    ):
        prepare_data_mock.return_value = None, None
        already_inferred_mock.return_value = False
        lda_mock.return_value = None
        self.lda.infer_model(self.timeline, '111')
        lda_mock.assert_called_once()
        logger_mock.called_with('Inferring LDA...')
        assert generate_html_mock.called
        assert not print_terms_mock.called

    def test_model_is_already_inferred(self):
        result = self.lda.model_is_already_inferred(self.timeline, '111')
        assert result is True

    def test_model_is_not_already_inferred(self):
        result = self.lda.model_is_already_inferred(self.timeline, '222')
        assert result is False

    @patch('src.classes.lda.LDA.make_bigrams')
    @patch('src.classes.lda.LDA.make_bag_of_words')
    def test_prepare_data(self, make_bow_mock, make_bigrams_mock):
        self.lda.use_bigrams = False
        self.lda.prepare_data(self.timeline)
        make_bow_mock.assert_called_once()
        assert not make_bigrams_mock.called

    @patch('src.classes.lda.LDA.make_bigrams')
    @patch('src.classes.lda.LDA.make_bag_of_words')
    def test_prepare_data_use_bigrams(self, make_bow_mock, make_bigrams_mock):
        self.lda.use_bigrams = True
        self.lda.prepare_data(self.timeline)
        make_bow_mock.assert_called_once()
        make_bigrams_mock.assert_called_once()
