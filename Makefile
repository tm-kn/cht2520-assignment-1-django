flake8:
	tox -e flake8

isort:
	tox -e isort

yapf:
	tox -e yapf

lint: isort flake8 yapf

test:
	tox -e py36

static:
	npm run build

.PHONY: flake8 isort lint test static
