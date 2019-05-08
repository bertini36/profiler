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

Make commands
```bash
make gettimelines timelines=Albert_Rivera,sanchezcastejon
make cleantimelines timelines=Albert_Rivera,sanchezcastejon
```

Python
```python
from profiler import Profiler

Profiler.get_timelines(users='Pablo_Iglesias_,pablocasado_')
Profiler.clean_timelines(users='Pablo_Iglesias_,pablocasado_')
```

## Next work

- Preprocessing textual data
- Find main topics of an user using Latent Dirichlet Allocation algorithm
- Show results using pyLDAvis
- Postgres backend with SQLAlchemist
- Make async providers and backends to work with asyncio
