PYTHON = python
VENV_DIR = venv

install:
	$(PYTHON) -m pip install -r requirements.txt

venv:
	$(PYTHON) -m venv $(VENV_DIR)

.PHONY: create_db
create_db:
	alembic upgrade head

.PHONY: tests
tests:
	$(PYTHON) -m pytest --cov-config=.coveragerc -p pytest_cov --cov=app --cov-append --cov-report=html app/tests/


