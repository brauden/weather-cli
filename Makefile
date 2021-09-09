install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint:
	pylint --disable=R,C weather_cli.py

test:
	python -m pytest -vv

all:
	install lint test