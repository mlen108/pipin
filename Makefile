SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo "    make release    | Release to PyPI."
	@echo "    make test       | Run the tests."
	@echo "    make test-nocov | Run the tests without coverage."

release:
	python setup.py register sdist upload

test:
	@coverage run ./setup.py test
	@coverage report --show-missing

test-nocov:
	python setup.py test
