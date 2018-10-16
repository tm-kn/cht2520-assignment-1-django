flake8:
	tox -e flake8

isort:
	tox -e isort

lint: isort flake8

test:
	tox -e py36

.PHONY: flake8 isort lint test
