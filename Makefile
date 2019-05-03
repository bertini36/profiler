DOCKER_COMPOSE = docker-compose -f docker-compose.yml
DRUN = $(DOCKER_COMPOSE) run --rm
PROFILER = $(DRUN) --entrypoint python profiler profiler.py

build:
	$(DOCKER_COMPOSE) build

runmongo:
	$(DRUN) mongodb

shell:
	$(DOCKER_COMPOSE) exec profiler bash

gettimelines:
	$(PROFILER) get_timelines $(timelines)
