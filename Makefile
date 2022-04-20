.PHONY: run
PROJECT ?= yuan
PYENV_NAME = .venv
SHELL := /bin/bash

##############################
# targets
##############################

run:
	@read -p "Enter Flask Secret Key:" FLASK_SECRET_KEY; \
    echo "$FLASK_SECRET_KEY" | docker secret create FLASK_SECRET_KEY
	@read -p "Enter MD email password Key:" MD_EMAIL_PASS; \
    echo "$MD_EMAIL_PASS" | docker secret create MD_EMAIL_PASS
	@echo
	sudo docker-compose build
	@echo
	sudo docker stack deploy --compose-file=docker-compose.yml md_backend
	@echo "- DONE: $@"
