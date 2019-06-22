# Profiler
[![Build Status](https://api.travis-ci.org/bertini36/profiler.svg?branch=master)](https://travis-ci.org/bertini36/profiler)
[![codecov](https://codecov.io/gh/bertini36/profiler/branch/master/graph/badge.svg)](https://codecov.io/gh/bertini36/profiler)

Profiler tries to identify main topics in personal Twitter timelines using 
<a href="http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf">LDA
 topic models algorithm</a> in a easy way for simple exploratory purposes
 
## Prerequisites

If you don’t have Docker installed, follow the instructions for your OS:

- On Mac OS X, you’ll need [Docker for Mac](https://docs.docker.com/docker-for-mac/)
- On Windows, you’ll need [Docker for Windows](https://docs.docker.com/docker-for-windows/)
- On Linux, you’ll need [docker-engine](https://docs.docker.com/engine/installation/)

And aditionally install [Docker compose](https://docs.docker.com/compose/install/)

## Usage

### Basic usage

**Build environment**
```bash
make build
```

**Run environment**
```bash
make up
```

**Stop environment**
```bash
make down
```

### Configurations
Set Mongo configs and Twitter API keys in `.env` file using `.env-sample` file
```bash
cp .env-sample .env
vim .env
```

**Download timeline, clean tweets and find topics**

Make commands
```bash
make get_timelines timelines=Albert_Rivera,sanchezcastejon
make clean_timelines timelines=Albert_Rivera,sanchezcastejon
make find_topics timelines=Albert_Rivera,sanchezcastejon n_topics=5
```
Run all steps:
```bash
make run_all timelines=Albert_Rivera,sanchezcastejon n_topics=5
```

Python
```python
from src.profiler import Profiler

Profiler.get_timelines(users='Pablo_Iglesias_,pablocasado_')
Profiler.clean_timelines(users='Pablo_Iglesias_,pablocasado_')
Profiler.find_topics(users='Pablo_Iglesias_,pablocasado_', n_topics=5)
```
Run all with the same command:
```python
Profiler.run_all(users='Pablo_Iglesias_,pablocasado_', n_topics=5)
```

And now you have time to take a coffe ☕️️️☕️☕️️️

### Algorithm configs

You can customize some algorithm technical configs at `src/settings.py`

## Development

To work with this codebase you'll need to clone the repository and build the docker image:

```bash
git clone git@github.com:bertini36/profiler
cd profiler
make build
```

To run tests and lint code run the following scripts:

```bash
make run_tests
make run_lint
```

### Results screenshot

<p align="center"><img src="https://github.com/bertini36/profiler/blob/master/img/photo.png"/></p>

<p align="center">&mdash; Built with :heart: from Mallorca &mdash;</p>
