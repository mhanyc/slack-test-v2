VE ?= ve
PIP ?= $(VE)/bin/pip
WHEEL_VERSION ?=  0.37.1
PIP_VERSION ?= 21.3.1
REQUIREMENTS ?= src/requirements.txt
SRC_DIR ?= src

create:
	rm -rf $(VE)
	python3 -m venv $(VE)
	$(PIP) install wheel==$(WHEEL_VERSION)
	$(PIP) install pip==$(PIP_VERSION)
	$(PIP) install --requirement $(REQUIREMENTS)

clean:
	rm -rf ve

.PHONY: pylint
pylint:
	python -m pylint "$(SRC_DIR)"

# wrapper for pep8, pyflakes and circular complexity
flake8:
	python -m flake8 "$(SRC_DIR)"

# runs all linting tools - build will fail if linter has any complaints
lint: flake8 pylint
	@echo "Running static analysis tools."

test:
	python tests/test_handler.py
