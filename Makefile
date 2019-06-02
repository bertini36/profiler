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

run_lint:
	echo "==> Sorting Python imports..."
	$(DRUN) --entrypoint "isort --recursive --apply src tests" profiler
	echo "==> Linting..."
	$(DRUN) --entrypoint "pylint src tests" profiler

run_tests:
	$(DRUN) --entrypoint "pytest --cov-report term --cov=src/" tests
	$(DRUN) --entrypoint "py3clean ." tests
	$(DRUN) --entrypoint "rm -rf .pytest_cache/" tests
	$(DRUN) --entrypoint "rm -rf .coverage" tests
