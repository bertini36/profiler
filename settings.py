# -*- coding: UTF-8 -*-

import environ

env = environ.Env()
environ.Env.read_env('.env')

# MONGO
# ******************************************************************************
MONGO_URL = env.str('MONGO_URL', default='mongodb')
MONGO_PORT = env.int('MONGO_PORT', default=27017)
MONGO_DB = env.str('MONGO_DB', default='profiler_db')
USE_EXISTING_DATABASE = True

# TWITTER
# ******************************************************************************
TWITTER_PUBLIC_KEY = env('TWITTER_PUBLIC_KEY')
TWITTER_SECRET_KEY = env('TWITTER_SECRET_KEY')
TWITTER_ACCESS_TOKEN = env('TWITTER_ACCESS_TOKEN')
TWITTER_SECRET_TOKEN = env('TWITTER_SECRET_TOKEN')
FILTER_RTS = False

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
REPLACE_PHONE_NUMBERS = True
FILTER_PHONE_NUMBERS = True
REPLACE_NUMBERS = True
FILTER_NUMBERS = True
REPLACE_DIGITS = True
FILTER_DIGITS = True
REPLACE_EMOJIS = True
FILTER_EMOJIS = True
REMOVE_PUNCT = True,
REMOVE_MULTIPLE_SPACES = True
TO_LOWER = True
FILTER_STOPWORDS = True
FILTER_EMPTY_ROWS = True

# LDA
# ******************************************************************************
LDA_N_PASSES = 500
LDA_USE_BIGRAMS = True
LDA_MIN_DF = 0
