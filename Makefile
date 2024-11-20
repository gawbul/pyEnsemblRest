freeze:
	poetry lock

install:
	poetry install --sync

unit-test:
	poetry run pytest -v

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
