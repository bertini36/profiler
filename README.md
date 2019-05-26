# Profiler
[![Build Status](https://api.travis-ci.org/bertini36/profiler.svg?branch=master)](https://travis-ci.org/bertini36/profiler)
[![codecov](https://codecov.io/gh/bertini36/profiler/branch/master/graph/badge.svg)](https://codecov.io/gh/bertini36/profiler)

Profiler tries to identify main topics in personal Twitter timelines using 
<a href="http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf">LDA
 topic models algorithm</a> in a easy way for simple exploratory purposes

## Usage

### Basic usage

**Run environment**
```bash
make build
make up
```

**Download and clean tweets**

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
from profiler import Profiler

Profiler.get_timelines(users='Pablo_Iglesias_,pablocasado_')
Profiler.clean_timelines(users='Pablo_Iglesias_,pablocasado_')
Profiler.find_topics(users='Pablo_Iglesias_,pablocasado_', n_topics=5)
```
Run all with the same command:
```python
Profiler.run_all(users='Pablo_Iglesias_,pablocasado_', n_topics=5)
```

And now you have time to take a coffe ☕️

### Algorithm configs

You can customize some algorithm technical configs at `settings.py`

### Testing

```bash
make run_tests
```

### Results screenshot

<p align="center"><img src="https://github.com/bertini36/profiler/blob/master/img/photo.png"/></p>
