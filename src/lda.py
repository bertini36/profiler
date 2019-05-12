# -*- coding: UTF-8 -*-

from pprint import pprint

import pandas as pd
from gensim import corpora
from gensim.models.ldamulticore import LdaMulticore
from gensim.models.phrases import Phrases, Phraser
from loguru import logger

from .exceptions import TimelineDoesNotExist

"""
TODO:
    - Generate HTML graphics
    - Use unanimity and threshold
    - Show progress using a versbose param
    - Save results in a optimum way to don't recalculate
"""


class Sentences:

    def __init__(self, texts):
        self.texts = texts

    def __iter__(self):
        for text in self.texts:
            yield text


class LDA:

    def __init__(
        self, storage_backend, n_topics=5, n_passes=500,
        use_bigrams=False, min_df=50, threshold=0.5, unanimity=0.3
    ):
        logger.info(
            f'Latent Dirichlet Allocation with n_topics={n_topics}, '
            f'n_passes={n_passes}, use_bigrams={use_bigrams},'
            f' min_df={min_df}, threshold={threshold}, '
            f'unanimity={unanimity} and using {storage_backend}'
        )
        self._storage_backend = storage_backend
        self.n_topics = n_topics
        self.n_passes = n_passes
        self.use_bigrams = use_bigrams
        self.min_df = min_df
        self.threshold = threshold
        self.unanimity = unanimity

    def run(self, username: str, save: bool = True):
        screen_name = f'@{username}' if '@' not in username else username
        logger.info(f'Run LDA for {screen_name} timeline')
        with self._storage_backend as backend:
            timeline = backend.get_timeline(screen_name)
            if not timeline:
                raise TimelineDoesNotExist(
                    f'There is no timeline for {screen_name} saved in '
                    f'{backend}. Please first, download it'
                )
            bow, dictionary = self.prepare_data(timeline)
            logger.info('Inferring LDA...')
            lda = LdaMulticore(
                bow,
                id2word=dictionary,
                num_topics=self.n_topics,
                passes=self.n_passes,
                random_state=0,
            )
            self.print_topics(lda)

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

    def print_topics(self, model: LdaMulticore):
        topics = []
        for topic in model.print_topics(num_topics=self.n_topics, num_words=10):
            topics.append([
                (s.split('*\"')[1].split('\"')[0], float(s.split('*\"')[0]))
                for s in str(topic[1]).split('+ ')
            ])
        pprint(topics)
