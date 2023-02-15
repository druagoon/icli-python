export LC_ALL=en_US.UTF-8

.DEFAULT_GOAL := motto
SHELL := /bin/bash

GIT := git
PROJECT_DIR := $(shell cd `dirname "$0"`; pwd)
VENV := .venv
VENV_BIN := $(VENV)/bin
PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
PIP_SYNC := $(VENV_BIN)/pip-sync
PIP_COMPILE := $(VENV_BIN)/pip-compile
PYLINT:= $(VENV_BIN)/pylint
ISORT := $(VENV_BIN)/isort
BLACK := $(VENV_BIN)/black
RUFF := $(VENV_BIN)/ruff

define compile_one
	$(eval r_txt := $(addsuffix .txt,$(basename $(1))))
	$(PIP_COMPILE) --resolver=backtracking -o "$(r_txt)" "$(1)"
endef

define compile_all
	$(foreach v,$(wildcard requirements/*.in),$(call compile_one,$(v)))
	$(PIP_COMPILE) --resolver=backtracking -o requirements/pyproject.txt pyproject.toml
endef

.PHONY: motto
motto:
	@if [ -f .motto ]; then cat .motto; fi

.PHONY: init
init:
	if [ ! -d "$(VENV)" ]; then $(PYTHON) -m venv --copies $(VENV); fi
	$(PIP) install -r requirements/tools.txt
	if [ ! -f ".git/hooks/pre-commit" ]; then $(VENV_BIN)/pre-commit install; fi
	if [ ! -f ".pre-commit-config.yaml" ]; then $(VENV_BIN)/pre-commit sample-config > .pre-commit-config.yaml; fi

.PHONY: install
install:
	$(PIP) install -U pip
	$(PIP) install -r requirements/all.txt

.PHONY: sync
sync:
	$(PIP) install -U pip
	$(PIP_SYNC) requirements/all.txt

.PHONY: compile
compile:
	@echo "Updating requirements/*.txt files using pip-compile"
	$(call compile_all)

.PHONY: upgrade
upgrade:
	find requirements/ -name '*.txt' ! -name 'all.txt' -type f -delete
	$(MAKE) compile

.PHONY: fmt
fmt:
	$(RUFF) check --fix .
	$(ISORT) .
	$(BLACK) .

.PHONY: lint
lint:
	$(RUFF) check .
	$(ISORT) --check-only --diff --color .
	$(BLACK) --check --diff --color .
