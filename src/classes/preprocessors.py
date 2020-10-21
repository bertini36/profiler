# -*- coding: UTF-8 -*-

import re
import string
from abc import ABC, abstractmethod

import nltk
import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from loguru import logger
from nltk.corpus import stopwords as nltk_stopwords
from stop_words import LANGUAGE_MAPPING, get_stop_words

from .decorators import timeit
from .exceptions import TimelineDoesNotExist

# Sources:
# - https://github.com/jfilter/clean-text/
# - https://github.com/kvvzr/python-emoji-regex

CURRENCIES = {
    '$': 'USD',
    'zł': 'PLN',
    '£': 'GBP',
    '¥': 'JPY',
    '฿': 'THB',
    '₡': 'CRC',
    '₦': 'NGN',
    '₩': 'KRW',
    '₪': 'ILS',
    '₫': 'VND',
    '€': 'EUR',
    '₱': 'PHP',
    '₲': 'PYG',
    '₴': 'UAH',
    '₹': 'INR',
}
CURRENCY_REGEX = re.compile(
    f'({"|".join(re.escape(c) for c in CURRENCIES.keys())})+'
)
PUNCTUATION = list(string.punctuation) + [
    '?',
    '¿',
    '¡',
    '!',
    '-',
    '->',
    '<-',
    '→',
    '—',
]
PUNCTUATION.remove('<')
PUNCTUATION.remove('>')
PUNCTUATION_REGEX = re.compile(
    f'({"|".join(re.escape(p) for p in PUNCTUATION)})'
)

MENTION_REGEX = re.compile(
    r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)'
)
EMAIL_REGEX = re.compile(
    r'(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w'
    r'+-]@(?:\w-?)*?\w+(\.([a-z]{2,})){1,3}(?:$|(?=\b))',
    flags=re.IGNORECASE | re.UNICODE,
)

NUMBERS_REGEX = re.compile(
    r'(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)'
    r'|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))'
)

LINEBREAK_REGEX = re.compile(r'((\r\n)|[\n\v])+')
MULTI_WHITESPACE_TO_ONE_REGEX = re.compile(r'\s+')
NONBREAKING_SPACE_REGEX = re.compile(r'(?!\n)\s+')

# source: https://gist.github.com/dperini/729294
URL_REGEX = re.compile(
    r'(?:^|(?<![\w\/\.]))'
    r'(?:(?:https?:\/\/|ftp:\/\/|www\d{0,3}\.))'
    r'(?:\S+(?::\S*)?@)?'
    r'(?:'
    r'(?!(?:10|127)(?:\.\d{1,3}){3})'
    r'(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})'
    r'(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})'
    r'(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])'
    r'(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}'
    r'(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))'
    r'|'
    r'(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)'
    r'(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*'
    r'(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))'
    r')'
    r'(?::\d{2,5})?'
    r'(?:\/[^\)\]\}\s]*)?',
    flags=re.UNICODE | re.IGNORECASE,
)

strange_double_quotes = [
    '«',
    '‹',
    '»',
    '›',
    '„',
    '“',
    '‟',
    '”',
    '❝',
    '❞',
    '❮',
    '❯',
    '〝',
    '〞',
    '〟',
    '＂',
]
strange_single_quotes = ['‘', '‛', '’', '❛', '❜', '`', '´', '‘', '’']
DOUBLE_QUOTE_REGEX = re.compile('|'.join(strange_double_quotes))
SINGLE_QUOTE_REGEX = re.compile('|'.join(strange_single_quotes))

with open('/code/src/classes/emojis.txt') as f:
    EMOJIS_REGEX = re.compile(''.join(f.readlines()).strip())


class Preprocessor(ABC):
    @abstractmethod
    def run(
        self,
        user: str,
        save: bool = True,
        replace_mentions: bool = True,
        filter_mentions: bool = True,
        replace_emails: bool = True,
        filter_emails: bool = True,
        replace_currencies: bool = True,
        filter_currencies: bool = True,
        replace_urls: bool = True,
        filter_urls: bool = True,
        replace_numbers: bool = True,
        filter_numbers: bool = True,
        replace_digits: bool = True,
        filter_digits: bool = True,
        replace_emojis: bool = True,
        filter_emojis: bool = True,
        remove_punct: bool = True,
        remove_multiple_spaces: bool = True,
        to_lower: bool = True,
        filter_stopwords: bool = True,
        filter_empty_rows: bool = True,
    ) -> dict:
        pass


class MyPreprocessor(Preprocessor):
    def __init__(self, storage_backend):
        self._storage_backend = storage_backend
        nltk.download('stopwords')

    @timeit
    def run(
        self,
        user: str,
        save: bool = True,
        replace_mentions: bool = True,
        filter_mentions: bool = True,
        replace_emails: bool = True,
        filter_emails: bool = True,
        replace_currencies: bool = True,
        filter_currencies: bool = True,
        replace_urls: bool = True,
        filter_urls: bool = True,
        replace_numbers: bool = True,
        filter_numbers: bool = True,
        replace_digits: bool = True,
        filter_digits: bool = True,
        replace_emojis: bool = True,
        filter_emojis: bool = True,
        remove_punct: bool = True,
        remove_multiple_spaces: bool = True,
        to_lower: bool = True,
        filter_stopwords: bool = True,
        filter_empty_rows: bool = True,
    ) -> dict:
        """
        This function gets a timeline from storage backend and
        clean text of each tweet for future procedures
        :param user: Twitter username
        :param save: If True cleaned timeline will be saved at backend storage
        :param replace_mentions: Replace mentions with <MENTION>
        :param filter_mentions: Filter tweet <MENTION>s
        :param replace_emails: Replace mentions with <EMAIL>
        :param filter_emails: Filter tweet <EMAIL>s
        :param replace_currencies: Replace mentions with <CURRENCY>
        :param filter_currencies: Filter tweet <CURRENCY>s
        :param replace_urls: Replace mentions with <URL>
        :param filter_urls: Filter tweet <URLS>s
        :param replace_numbers: Replace mentions with <NUMBER>
        :param filter_numbers: Filter tweet <NUMBER>s
        :param replace_digits: Replace mentions with 0
        :param filter_digits: Filter tweet 0s
        :param replace_emojis: Replace mentions with <EMOJI>
        :param filter_emojis: Filter tweet <EMOJI>s
        :param remove_punct: Remove punctuation symbols
        :param remove_multiple_spaces: Remove joined spaces
        :param to_lower: To lower case result tweets
        :param filter_stopwords: Filter ``lang`` stopwords
        :param filter_empty_rows: Filter empty tweets after preprocessing
        """
        logger.info(f'Preprocessing {user} timeline')
        with self._storage_backend as backend:
            try:
                timeline = backend.get_timeline(user)
                if not timeline:
                    raise TimelineDoesNotExist(
                        f'There is no timeline for {user} saved in '
                        f'{backend}. Please first, download it'
                    )
                cleaned_timeline = self.clean_timeline(
                    timeline,
                    replace_mentions=replace_mentions,
                    filter_mentions=filter_mentions,
                    replace_emails=replace_emails,
                    filter_emails=replace_emails,
                    replace_currencies=replace_currencies,
                    filter_currencies=filter_currencies,
                    replace_urls=replace_urls,
                    filter_urls=filter_urls,
                    replace_numbers=replace_numbers,
                    filter_numbers=filter_numbers,
                    replace_digits=replace_digits,
                    filter_digits=filter_digits,
                    replace_emojis=replace_emojis,
                    filter_emojis=filter_emojis,
                    remove_punct=remove_punct,
                    remove_multiple_spaces=remove_multiple_spaces,
                    to_lower=to_lower,
                    filter_stopwords=filter_stopwords,
                    filter_empty_rows=filter_empty_rows,
                )
                if save:
                    backend.update_timeline(user, cleaned_timeline)
            except Exception as e:
                logger.error(e)
        return cleaned_timeline

    @staticmethod
    def clean_timeline(
        timeline: dict,
        replace_mentions: bool = True,
        filter_mentions: bool = True,
        replace_emails: bool = True,
        filter_emails: bool = True,
        replace_currencies: bool = True,
        filter_currencies: bool = True,
        replace_urls: bool = True,
        filter_urls: bool = True,
        replace_numbers: bool = True,
        filter_numbers: bool = True,
        replace_digits: bool = True,
        filter_digits: bool = True,
        replace_emojis: bool = True,
        filter_emojis: bool = True,
        remove_punct: bool = True,
        remove_multiple_spaces: bool = True,
        to_lower: bool = True,
        filter_stopwords: bool = True,
        filter_empty_rows: bool = True,
    ) -> dict:
        """
        This function will do all text
        transformations for each tweet in timeline
        """
        df = pd.DataFrame(
            timeline['tweets'], columns=['id', 'created_at', 'text']
        )
        logger.info(f'Preprocessing {df.shape[0]} tweets of {timeline["user"]}')
        if replace_mentions:
            df['text'] = df['text'].apply(
                MyPreprocessor.replace_mentions,
                args=('',) if filter_mentions else None,
            )
        if replace_emails:
            df['text'] = df['text'].apply(
                MyPreprocessor.replace_emails,
                args=('',) if filter_emails else None,
            )
        if replace_currencies:
            df['text'] = df['text'].apply(
                MyPreprocessor.replace_currencies,
                args=('',) if filter_currencies else None,
            )
        if replace_urls:
            df['text'] = df['text'].apply(
                MyPreprocessor.replace_urls, args=('',) if filter_urls else None
            )
        if replace_numbers:
            df['text'] = df['text'].apply(
                MyPreprocessor.replace_numbers,
                args=('',) if filter_numbers else None,
            )
        if replace_digits:
            df['text'] = df['text'].apply(
                MyPreprocessor.replace_digits,
                args=('',) if filter_digits else None,
            )
        if replace_emojis:
            df['text'] = df['text'].apply(
                MyPreprocessor.replace_emojis,
                args=('',) if filter_emojis else None,
            )
        if remove_punct:
            df['text'] = df['text'].apply(MyPreprocessor.remove_punct)
        if remove_multiple_spaces:
            df['text'] = df['text'].apply(MyPreprocessor.remove_multiple_spaces)
        if to_lower:
            df['text'] = df['text'].apply(lambda text: text.lower())
        if filter_stopwords:
            df['text'] = df['text'].apply(MyPreprocessor.filter_stopwords)
        if filter_empty_rows:
            mask = df.apply(MyPreprocessor.filter_empty_rows, axis=1)
            df = df[mask]
            logger.info(
                f'There are {df.shape[0]} not null tweets of {timeline["user"]}'
            )

        return {
            'user': timeline['user'],
            'tweets': timeline['tweets'],
            'cleaned_tweets': list(df.T.to_dict().values()),
        }

    @staticmethod
    def fix_strange_quotes(text: str) -> str:
        """
        Replace strange quotes, i.e., 〞with a single
        quote ' or a double quote " if it fits better
        """
        text = SINGLE_QUOTE_REGEX.sub("'", text)
        text = DOUBLE_QUOTE_REGEX.sub('"', text)
        return text

    @staticmethod
    def normalize_whitespace(text: str, no_line_breaks: bool = False) -> str:
        """
        Given ``text`` str, replace one or more spacings with a single space,
        and one or more line breaks with a single newline.
        Also strip leading/trailing whitespace.
        """
        if no_line_breaks:
            text = MULTI_WHITESPACE_TO_ONE_REGEX.sub(' ', text)
        else:
            text = NONBREAKING_SPACE_REGEX.sub(
                ' ', LINEBREAK_REGEX.sub(r'\n', text)
            )
        return text.strip()

    @staticmethod
    def replace_urls(text: str, replace_with: str = '<URL>') -> str:
        """
        Replace all URLs in ``text`` str with ``replace_with`` str
        """
        return URL_REGEX.sub(replace_with, text)

    @staticmethod
    def replace_mentions(text: str, replace_with: str = '<MENTION>') -> str:
        """
        Replace all mentions in ``text`` str with ``replace_with`` str
        """
        return MENTION_REGEX.sub(replace_with, text)

    @staticmethod
    def replace_emails(text: str, replace_with: str = '<EMAIL>') -> str:
        """
        Replace all emails in ``text`` str with ``replace_with`` str
        """
        return EMAIL_REGEX.sub(replace_with, text)

    @staticmethod
    def replace_numbers(text: str, replace_with: str = '<NUMBER>') -> str:
        """
        Replace all numbers in ``text`` str with ``replace_with`` str
        """
        return NUMBERS_REGEX.sub(replace_with, text)

    @staticmethod
    def replace_digits(text: str, replace_with: str = '0') -> str:
        """
        Replace all digits in ``text`` str with `
        `replace_with`` str, i.e., 123.34 to 000.00
        """
        return re.sub(r'\d', replace_with, text)

    @staticmethod
    def replace_currencies(text: str, replace_with: str = '<CURRENCY>') -> str:
        """
        Replace all currency symbols in ``text`` str with
        string specified by ``replace_with`` str.
        Args:
            text (str): raw text
            replace_with (str): if None (default), replace symbols with
                their standard 3-letter abbreviations
                (e.g. '$' with 'USD', '£' with 'GBP');
                otherwise, pass in a string with which to replace all symbols
                (e.g. "*CURRENCY*")
        Returns:
            str
        """
        if replace_with is None:
            for k, v in CURRENCIES.items():
                text = text.replace(k, v)
            return text
        else:
            return CURRENCY_REGEX.sub(replace_with, text)

    @staticmethod
    def replace_emojis(text: str, replace_with: str = '<EMOJI>') -> str:
        """
        Replace all emojis in ``text`` str with ``replace_with`` str
        """
        return EMOJIS_REGEX.sub(replace_with, text)

    @staticmethod
    def remove_punct(text: str) -> str:
        """
        Replace punctuations from ``text`` with whitespaces
        Args:
            text (str): raw text
        Returns:
            str
        """
        return PUNCTUATION_REGEX.sub(' ', text)

    @staticmethod
    def remove_multiple_spaces(text: str) -> str:
        """
        Replace multiple spaces by single one
        """
        return re.sub(' +', ' ', text)

    @staticmethod
    def get_stopwords(text):
        """
        Get stopwords using text language
        """
        try:
            lang = detect(text)
        except LangDetectException:
            lang = 'en'
        stopwords = []
        if lang in LANGUAGE_MAPPING:
            stopwords = get_stop_words(lang)
            try:
                stopwords.extend(nltk_stopwords.words(LANGUAGE_MAPPING[lang]))
            except OSError:
                # NLTK does not have lang stopwords
                pass
        return stopwords

    @staticmethod
    def filter_stopwords(text: str):
        """
        Filter language specified stopwords from ``text``
        """
        stopwords = MyPreprocessor.get_stopwords(text)
        filtered_words = [
            word for word in text.split() if word not in stopwords
        ]
        return ' '.join(filtered_words)

    @staticmethod
    def filter_empty_rows(row) -> bool:
        return True if row['text'] else False
