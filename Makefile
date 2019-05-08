DOCKER_COMPOSE = docker-compose -f docker-compose.yml
DRUN = $(DOCKER_COMPOSE) run --rm
PROFILER = $(DRUN) --entrypoint python profiler profiler.py

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down

runmongo:
	$(DRUN) mongodb

mongoshell:
	$(DOCKER_COMPOSE) exec mongodb mongo

gettimelines:
	$(PROFILER) get_timelines $(timelines)

cleantimelines:
	$(PROFILER) clean_timelines $(timelines)
