# profiler
The purpose of this project is to identify main topics in personal twitter 
timelines.

# Development environment

**1. System requirements**

- Install Python and virtualenv

- Install requirements
    
``pip install -r requirements.txt``

**2. Download code**

``https://github.com/bertini36/profiler``

**3. Set project variables**

- Create .env file and set variables as in .env-sample

``touch .env``

# Possible commands

``python profiler.py download_tweets --users Albert_Rivera,sanchezcastejon``

# Next work

- Preprocessing textual data
- Find main topics of an user using Latent Dirichlet Allocation algorithm
- Show results using pyLDAvis
