SHELL := /bin/bash

install_dependencies:
	python3.10 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	source venv/bin/activate && pre-commit install --hook-type pre-push --hook-type post-checkout --hook-type pre-commit

run_precommit:
	pre-commit run --all-files

# by writing "make run_test" in the terminal all the tests in the directory "tests/" will run.

VENV_NAME = venv

activate:
	source $(VENV_NAME)/bin/activate

TEST_DIR = tests

run_test: activate
	pytest $(TEST_DIR)
