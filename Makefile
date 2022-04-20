.PHONY: run
SHELL := /bin/bash

##############################
# targets
##############################

run:
	@echo "Please enter FLASK_SECRET_KEY:" \
	@read FLASK_SECRET_KEY; \
    echo "$$FLASK_SECRET_KEY" | docker secret create FLASK_SECRET_KEY
    @echo "Please enter MD_EMAIL_PASS:" \
    @read MD_EMAIL_PASS; \
    echo "$(MD_EMAIL_PASS)" | docker secret create MD_EMAIL_PASS
	@echo
	sudo docker-compose build
	@echo
	sudo docker stack deploy --compose-file=docker-compose.yml md_backend
	@echo "- DONE: $@"
