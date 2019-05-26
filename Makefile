DOCKER_COMPOSE = docker-compose -f docker-compose.yml
DRUN = $(DOCKER_COMPOSE) run --rm
PROFILER = $(DRUN) --entrypoint python profiler profiler.py

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down

run_mongo:
	$(DRUN) mongodb

mongo_shell:
	$(DOCKER_COMPOSE) exec mongodb mongo

get_timelines:
	$(PROFILER) get_timelines $(timelines)

clean_timelines:
	$(PROFILER) clean_timelines $(timelines)

find_topics:
	$(PROFILER) find_topics $(timelines) $(n_topics)

run_all:
	$(PROFILER) run_all $(timelines) $(n_topics)

run_tests:
	$(DRUN) --entrypoint pytest tests
