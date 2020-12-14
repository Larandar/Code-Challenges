PYTEST_ADDOPTS="--flake8 --black --isort --pydocstyle"
PYTEST_WATCH_ARGS=--clear --spool=300 -q
PYTEST_ARGS=--failed-first

PERL_BENCHMARK='/^(.*) call.*Day(\d+)Part(\d+).*input_of_day/ && print "Day $$2 $$3/2: $$1\n"'

clean:
	rm -rf inputs

test:
	PYTEST_ADDOPTS=$(PYTEST_ADDOPTS) pytest

run:
	pytest-watch $(PYTEST_WATCH_ARGS) -- $(PYTEST_ARGS)

benchmark:
	@pytest --durations=0 -vv | perl -n -e$(PERL_BENCHMARK)