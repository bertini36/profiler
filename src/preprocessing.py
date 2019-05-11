# -*- coding: UTF-8 -*-

import re
import string

import pandas as pd
from loguru import logger

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
PUNCTUATION = list(string.punctuation) + ['?', '¿', '¡', '!']
PUNCTUATION.remove('<')
PUNCTUATION.remove('>')
PUNCT_REGEX = re.compile(
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

PHONE_REGEX = re.compile(
    r'(?:^|(?<=[^\w)]))(\+?1[ .-]?)?(\(?\d{3}\)?[ .-]?)?'
    r'(\d{3}[ .-]?\d{4})(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W))'
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
    r'(?:\S+(?::\S*)?@)?' r'(?:'
    r'(?!(?:10|127)(?:\.\d{1,3}){3})'
    r'(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})'
    r'(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})'
    r'(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])'
    r'(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}'
    r'(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))'
    r'|'
    r'(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)'
    r'(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*'
    r'(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))' r')'
    r'(?::\d{2,5})?'
    r'(?:\/[^\)\]\}\s]*)?',
    flags=re.UNICODE | re.IGNORECASE,
)

strange_double_quotes = [
    '«', '‹', '»', '›', '„', '“', '‟', '”',
    '❝', '❞', '❮', '❯', '〝', '〞', '〟', '＂',
]
strange_single_quotes = ['‘', '‛', '’', '❛', '❜', '`', '´', '‘', '’']
DOUBLE_QUOTE_REGEX = re.compile('|'.join(strange_double_quotes))
SINGLE_QUOTE_REGEX = re.compile('|'.join(strange_single_quotes))

with open('src/emojis.txt') as f:
    EMOJIS_REGEX = re.compile(
        ''.join(f.readlines()).strip()
    )


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

    @staticmethod
    def clean_timeline(timeline: dict) -> dict:
        """
        This function will do all text
        transformations for each tweet in timeline
        """
        df = pd.DataFrame(timeline['tweets'], columns=['created_at', 'text'])
        logger.info(f'Preprocessing {df.shape[0]} tweets of {timeline["user"]}')
        df['text'] = df['text'].apply(Preprocessor.replace_mentions)
        df['text'] = df['text'].apply(Preprocessor.replace_emails)
        df['text'] = df['text'].apply(Preprocessor.replace_currency_symbols)
        df['text'] = df['text'].apply(Preprocessor.replace_urls)
        df['text'] = df['text'].apply(Preprocessor.replace_phone_numbers)
        df['text'] = df['text'].apply(Preprocessor.replace_numbers)
        df['text'] = df['text'].apply(Preprocessor.replace_digits)
        df['text'] = df['text'].apply(Preprocessor.replace_emojis)
        df['text'] = df['text'].apply(Preprocessor.remove_punct)
        df['text'] = df['text'].apply(Preprocessor.remove_multiple_spaces)
        df['text'] = df['text'].apply(lambda text: text.lower())
        mask = df.apply(Preprocessor.filter_empty_rows, axis=1)
        df = df[mask]
        logger.info(
            f'There are {df.shape[0]} not null tweets of {timeline["user"]}'
        )
        return {
            'user': timeline['user'],
            'tweets': timeline['tweets'],
            'cleaned_tweets': list(df.T.to_dict().values())
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
    def replace_phone_numbers(text: str, replace_with: str = '<PHONE>') -> str:
        """
        Replace all phone numbers in ``text`` str with ``replace_with`` str
        """
        return PHONE_REGEX.sub(replace_with, text)

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
    def replace_currency_symbols(text: str, replace_with: str = '<CUR>') -> str:
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
        Replace punctuations from ``text`` with whitespaces.
        Args:
            text (str): raw text
        Returns:
            str
        """
        return PUNCT_REGEX.sub(' ', text)

    @staticmethod
    def remove_multiple_spaces(text: str) -> str:
        """
        Replace multiple spaces by single one
        """
        return re.sub(' +', ' ', text)

    @staticmethod
    def filter_empty_rows(row) -> bool:
        return True if row['text'] else False
