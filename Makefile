SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo "    make release    | Release to PyPI."
	@echo "    make test       | Run the tests."

release:
	python setup.py register sdist upload
