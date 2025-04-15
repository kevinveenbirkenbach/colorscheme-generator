.PHONY: install test clean

install:
	python -m venv .venv
	. .venv/bin/activate && pip install .[test]

test:
	PYTHONPATH=src pytest

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
