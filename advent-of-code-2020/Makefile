PYTEST_ADDOPTS="--flake8 --black --isort --pydocstyle"

test:
	PYTEST_ADDOPTS=$(PYTEST_ADDOPTS) pytest

run:
	pytest-watch --clear --ext=py,txt,csv --spool=300 -q