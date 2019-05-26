# Profiler
Profiler tries to identify main topics in personal twitter timelines using 
LDA topic models in a confortable and easy way for exploratory purposes

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
Run all steps:
```python
Profiler.make_all(users='Pablo_Iglesias_,pablocasado_', n_topics=5)
```

### Algorithm configs

You can customize some algorithm technical configs at `settings.py`

### Testing

```bash
make run_tests
```
