PYTHON = python
VENV_DIR = venv

install:
	$(PYTHON) -m pip install -r requirements.txt

venv:
	$(PYTHON) -m venv $(VENV_DIR)

.PHONY: lint_black
create_db:
	black .

.PHONY: lint_isort
create_db:
	isort .

.PHONY: lint_pylint
create_db:
	pylint ./app

.PHONY: create_db
create_db:
	alembic upgrade head

.PHONY: tests
tests:
	$(PYTHON) -m pytest -s --cov-config=.coveragerc -p pytest_cov --cov=app --cov-append --cov-report=html app/tests/


