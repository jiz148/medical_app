.PHONY: run
PROJECT ?= yuan
PYENV_NAME = .venv
SHELL := /bin/bash

##############################
# targets
##############################

run:
	@FLASK_SECRET_KEY ?= $(shell bash -c 'read -s -p "FLASK_SECRET_KEY: "') \
    echo "$(FLASK_SECRET_KEY)" | docker secret create FLASK_SECRET_KEY
	@FLASK_SECRET_KEY ?= $(shell bash -c 'read -s -p "MD_EMAIL_PASS: "') \
    echo "$(MD_EMAIL_PASS)" | docker secret create MD_EMAIL_PASS
	@echo
	sudo docker-compose build
	@echo
	sudo docker stack deploy --compose-file=docker-compose.yml md_backend
	@echo "- DONE: $@"
