# -*- coding: UTF-8 -*-

from environs import Env

# You can rename -env-sample for use hidden configs
env = Env()
env.read_env('.env')

# MONGO
# ******************************************************************************
MONGO_URL = 'mongodb'
MONGO_PORT = 27017
MONGO_DB = 'profiler_db'
USE_EXISTING_DATABASE = True

# TWITTER
# ******************************************************************************
TWITTER_PUBLIC_KEY = env('TWITTER_PUBLIC_KEY', default='')
TWITTER_SECRET_KEY = env('TWITTER_SECRET_KEY', default='')
TWITTER_ACCESS_TOKEN = env('TWITTER_ACCESS_TOKEN', default='')
TWITTER_SECRET_TOKEN = env('TWITTER_SECRET_TOKEN', default='')
FILTER_RTS = True

# PREPROCESSING
# ******************************************************************************
REPLACE_MENTIONS = True
FILTER_MENTIONS = True
REPLACE_EMAILS = True
FILTER_EMAILS = True
REPLACE_CURRENCIES = True
FILTER_CURRENCIES = True
REPLACE_URLS = True
FILTER_URLS = True
REPLACE_NUMBERS = True
FILTER_NUMBERS = True
REPLACE_DIGITS = True
FILTER_DIGITS = True
REPLACE_EMOJIS = True
FILTER_EMOJIS = True
REMOVE_PUNCT = True
REMOVE_MULTIPLE_SPACES = True
TO_LOWER = True
FILTER_STOPWORDS = True
FILTER_EMPTY_ROWS = True

# LDA
# ******************************************************************************
LDA_N_PASSES = 20
LDA_USE_BIGRAMS = True
LDA_MIN_DF = 0
