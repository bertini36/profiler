# -*- coding: UTF-8 -*-

import pickle
import warnings
from pprint import pprint

import pandas as pd
from gensim import corpora
from gensim.models.ldamulticore import LdaMulticore
from gensim.models.phrases import Phrases, Phraser
from loguru import logger

from .decorators import timeit
from .exceptions import TimelineDoesNotExist

with warnings.catch_warnings():
    warnings.simplefilter('ignore', DeprecationWarning)
    import pyLDAvis.gensim


class Sentences:

    def __init__(self, texts):
        self.texts = texts

    def __iter__(self):
        for text in self.texts:
            yield text


class LDA:

    def __init__(
        self, storage_backend, n_topics=5,
        n_passes=200, use_bigrams=False, min_df=50
    ):
        logger.info(
            f'Latent Dirichlet Allocation with n_topics={n_topics}, '
            f'n_passes={n_passes}, use_bigrams={use_bigrams},'
            f' min_df={min_df} and using {storage_backend}'
        )
        self._storage_backend = storage_backend
        self.n_topics = n_topics
        self.n_passes = n_passes
        self.use_bigrams = use_bigrams
        self.min_df = min_df

    @timeit
    def run(self, user: str, save: bool = True, verbose: bool = False):
        """
        This function infers a LDA topic model of user specified
        :param user: Username to construct model
        :param save: If True, results will be saved at storage_backend
        :param verbose: Shows more used terms in a print
        """
        logger.info(f'Run LDA for {user} timeline')
        with self._storage_backend as backend:
            timeline = self.__class__.get_timeline(user, backend)
            exec_key = self.get_execution_key(user)
            model = self.infer_model(timeline, exec_key, verbose)
            if model and save:
                self.save_model(model, timeline)

    @staticmethod
    def get_timeline(user: str, backend):
        timeline = backend.get_timeline(user)
        if not timeline:
            raise TimelineDoesNotExist(
                f'There is no timeline for {user} saved in '
                f'{backend}. Please first, download it'
            )
        return timeline

    def infer_model(self, timeline: dict, exec_key, verbose: bool = False):
        bow, dictionary = self.prepare_data(timeline)
        if self.__class__.model_is_already_inferred(timeline, exec_key):
            logger.info('Model is already inferred')
            model = pickle.loads(timeline['models'][exec_key])
        else:
            logger.info('Inferring LDA...')
            try:
                model = LdaMulticore(
                    bow,
                    id2word=dictionary,
                    num_topics=self.n_topics,
                    passes=self.n_passes,
                    random_state=0,
                )
            except ValueError as e:
                error = 'cannot compute LDA over an empty collection (no terms)'
                if str(e) == error:
                    logger.error(
                        'Cannot compute LDA, there are no terms enough. '
                        'Maybe you need to decrease LDA_MIN_DF setting'
                    )
                return None
        if verbose:
            self.print_terms(model)
        self.generate_html(model, bow, dictionary, timeline['user'])
        return model

    @staticmethod
    def model_is_already_inferred(timeline: dict, exec_key: str):
        return 'models' in timeline and exec_key in timeline['models']

    def get_execution_key(self, user: str):
        return f'{user}-t{self.n_topics}-p{self.n_passes}'

    def prepare_data(self, timeline: dict) -> (list, corpora.Dictionary):
        df = pd.DataFrame(
            timeline['cleaned_tweets'],
            columns=['id', 'created_at', 'text']
        )
        logger.info(f'Preparing data for LDA...({df.shape[0]} tweets)')
        texts = Sentences([text.split() for text in list(df['text'])])
        if self.use_bigrams:
            texts = self.make_bigrams(texts)
        return self.make_bag_of_words(texts)

    @staticmethod
    def make_bigrams(texts: iter) -> iter:
        logger.info('Creating bigrams...')
        bigrams = Phraser(Phrases(texts))
        return Sentences(bigrams[texts])

    def make_bag_of_words(self, texts: iter) -> (list, corpora.Dictionary):
        dictionary = corpora.Dictionary(texts)
        dictionary.filter_extremes(no_below=self.min_df)
        dictionary.filter_n_most_frequent(2)
        bow = list(map(dictionary.doc2bow, texts))
        return bow, dictionary

    def print_terms(self, model: LdaMulticore):
        topics = []
        for topic in model.print_topics(num_topics=self.n_topics, num_words=10):
            topics.append([
                (s.split('*\"')[1].split('\"')[0], float(s.split('*\"')[0]))
                for s in str(topic[1]).split('+ ')
            ])
        pprint(topics)

    def generate_html(
        self, model: LdaMulticore, bow: list,
        dictionary: corpora.Dictionary, user: str
    ):
        data = pyLDAvis.gensim.prepare(model, bow, dictionary)
        pyLDAvis.save_html(
            data,
            f'output/{self.get_execution_key(user)}.html'
        )

    def save_model(self, model: LdaMulticore, timeline: dict):
        logger.info(f'Saving lda model at {self._storage_backend}')
        serialized_model = pickle.dumps(model)
        exec_key = self.get_execution_key(timeline['user'])
        if 'models' not in timeline:
            timeline['models'] = {}
        timeline['models'][exec_key] = serialized_model
        self._storage_backend.update_timeline(timeline['user'], timeline)
