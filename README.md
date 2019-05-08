# profiler
profiler purpose is to identify main topics in personal twitter timelines.

# Basic usage

```
make build
make up
```

```
make gettimelines timelines=Albert_Rivera,sanchezcastejon
make cleantimelines timelines=Albert_Rivera,sanchezcastejon
```

# Next work

- Preprocessing textual data
- Find main topics of an user using Latent Dirichlet Allocation algorithm
- Show results using pyLDAvis
- Postgres backend with SQLAlchemist
- Make async providers and backends to work with asyncio
