freeze:
	poetry lock

install:
	poetry install --sync

unit-test:
	poetry run pytest -v -m "not live"

ci-test:
	poetry run pytest -v --cov=pyensemblrest --cov-report lcov:./tests/lcov.info tests/

coverage:
	poetry run coveralls

type-check:
	poetry run mypy . --no-incremental

lint:
	poetry run ruff check . --fix

format:
	poetry run ruff format .

install-poetry:
	curl -sSL https://install.python-poetry.org | python3 - --version=$(cat .poetry-version)

uninstall-poetry:
	curl -sSL https://install.python-poetry.org | python3 - --uninstall
