PYTHON = python3
NAME = snake_game

help:
	@echo \"make setup\" - setup project
	@echo \"make install\" - install deps
	@echo \"make requirements\" - lock deps
	@echo \"make run\" - run 'snake game.py'

setup:
	\
	python3 -m venv .venv; \
	source .venv/bin/activate; \
	python3 -m pip install --upgrade pip;

install: requirements.txt
	python3 -m pip install -r requirements.txt

requirements:
	python -m pip freeze > requirements.txt

run: 
	$(PYTHON) -m 'snake game.py'