# -*- coding: UTF-8 -*-

import environ

env = environ.Env()
environ.Env.read_env('.env')

# MONGO
# ******************************************************************************
MONGO_URL = env('MONGO_URL', default='mongodb')
MONGO_PORT = env.int('MONGO_PORT', default=27017)
MONGO_DB = env('MONGO_DB', default='profiler_db')
USE_EXISTING_DATABASE = env.bool('USE_EXISTING_DATABASE', False)

# TWITTER
# ******************************************************************************
TWITTER_PUBLIC_KEY = env('TWITTER_PUBLIC_KEY')
TWITTER_SECRET_KEY = env('TWITTER_SECRET_KEY')
TWITTER_ACCESS_TOKEN = env('TWITTER_ACCESS_TOKEN')
TWITTER_SECRET_TOKEN = env('TWITTER_SECRET_TOKEN')
