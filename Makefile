APP = $(notdir $(CURDIR))
TAG = $(shell echo "$$(date +%F)-$$(git rev-parse --short HEAD)")
DOCKER_REPO = ghcr.io/managedkaos


help:
	@echo "Run make <target> where target is one of the following..."
	@echo
	@echo "  all                      - run requirements, lint, test, and build"
	@echo "  requirements             - install runtime dependencies"
	@echo "  development-requirements - install development dependencies"
	@echo "  pre-commit-install       - install pre-commit hooks"
	@echo "  pre-commit-update        - update pre-commit hooks"
	@echo "  pre-commit-run           - run pre-commit on all files"
	@echo "  pre-commit-clean         - remove pre-commit hooks"
	@echo "  lint                     - run flake8, pylint, black, and isort checks"
	@echo "  black                    - format code with black"
	@echo "  isort                    - sort imports with isort"

all: requirements lint up

development-requirements: requirements
	pip install --quiet --upgrade --requirement development-requirements.txt

pre-commit-install: development-requirements
	pre-commit install

pre-commit-update: development-requirements
	pre-commit autoupdate
	$(MAKE) pre-commit-run

pre-commit-run: development-requirements
	pre-commit run --all-files

x_pre-commit-clean:
	pre-commit uninstall

lint:
	flake8 --ignore=E501,E231 *.py
	pylint --errors-only *.py
	black --diff *.py
	isort --check-only --diff *.py

fmt: black isort

black:
	black *.py

isort:
	isort *.py

up:
	uvicorn main:app --host=0.0.0.0 --port=8000 --reload

.PHONY: help all requirements development-requirements \
	pre-commit-install pre-commit-update pre-commit-run pre-commit-clean \
	lint fmt black isort up
