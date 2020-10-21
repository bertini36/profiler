all: build

include .env
$(eval export $(shell sed -ne 's/ *#.*$//; /./ s/=.*$$// p' .env))

PROFILER = docker-compose run --rm -w /code/ --entrypoint "python src/profiler.py" profiler

service = profiler

.PHONY: build
build: ## build app
	@echo "📦 Building app"
	@docker-compose build --no-cache $(service)

run: ## run get-timelines, clean-timelines and find-topics
	$(PROFILER) run_all $(timelines) $(topics)

get-timelines: ## download timelines
	$(PROFILER) get_timelines $(timelines)

clean-timelines: ## timelines preprocessing
	$(PROFILER) clean_timelines $(timelines)

find-topics: ## find topics using LDA
	$(PROFILER) find_topics $(timelines) $(topics)

serve: ## run app
	@echo "🛫 Serving app"
	docker-compose up $(service)

down: ## shut down app
	@echo "🔌 Disconnecting"
	@docker-compose down

restart: ## restart a container
	@echo "↩️ Restarting"
	@docker-compose restart $(service)

connect: ## connect to a container
	@echo "🔞 Connecting to container"
	@docker-compose run $(service) /bin/bash

log: ## show container logs
	@echo "📋 Showing logs"
	@docker-compose logs -f --tail 100 $(service)

update-deps: ## update requirements files with last packages versions
	@echo "📥 Updating dependencies"
	@docker-compose run --rm --entrypoint sh profiler -c "pip-compile /code/requirements/dev.in --upgrade"

lint: ## lint code
	@echo "🔦 Linting code"
	@docker-compose run --rm --entrypoint sh profiler -c "black /code/ -t py38 --line-length 80 --skip-string-normalization"

test: ## run tests
	@echo "🏃‍ Running tests"
	@docker-compose run --rm --entrypoint sh profiler -c "cd /code/ && py.test tests --cov=src $(args)"

help: ## show make targets
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf " \033[36m%-20s\033[0m  %s\n", $$1, $$2}' $(MAKEFILE_LIST)
