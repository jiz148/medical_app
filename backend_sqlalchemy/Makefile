.PHONY: run
SHELL := /bin/bash

##############################
# targets
##############################

run:
	@read -p "Please enter FLASK_SECRET_KEY: " FLASK_SECRET_KEY \
	&& echo "$${FLASK_SECRET_KEY}" | docker secret create FLASK_SECRET_KEY -
	@read -p "Please enter MD_EMAIL_PASS: " MD_EMAIL_PASS \
	&& echo "$${MD_EMAIL_PASS}" | docker secret create MD_EMAIL_PASS -
	@echo
	docker-compose build
	@echo
	docker stack deploy --compose-file=docker-compose.yml md_backend
	@echo "- DONE: $@"
