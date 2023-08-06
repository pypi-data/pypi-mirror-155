.PHONY: run
run: build
	docker-compose run -p 127.0.0.1:8000:8000 --rm app /bin/bash

.PHONY: shell
shell:
	docker exec -it `docker ps | grep pythonlsi_app | cut -d" " -f1 | tail -n1` /bin/bash

.PHONY: build
build:
	docker-compose build

.PHONY: up
up: build
	docker-compose up

.PHONY: down
down:
	docker-compose down

.PHONY: format
format:
	npx mega-linter-runner --flavor python --fix
