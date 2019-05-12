# Profiler
Profiler purpose is to identify main topics in personal twitter timelines.

## Usage

### Basic usage

Run environment
```bash
make build
make up
```

Download and clean tweets:

**Make commands**
```bash
make gettimelines timelines=Albert_Rivera,sanchezcastejon
make cleantimelines timelines=Albert_Rivera,sanchezcastejon
make findtopics timelines=Albert_Rivera,sanchezcastejon n_topics=5
```

**Python**
```python
from profiler import Profiler

Profiler.get_timelines(users='Pablo_Iglesias_,pablocasado_')
Profiler.clean_timelines(users='Pablo_Iglesias_,pablocasado_')
Profiler.find_topics(users='Pablo_Iglesias_,pablocasado_', n_topics=5)

```

## Next work

- Show results using pyLDAvis
- Make tests
- Postgres backend with SQLAlchemist
