.PHONY: run-server

install-server-locally:
	rm -rf venv venv
	python -m venv venv
	. venv/bin/activate; pip install -r requirements/locked.txt

run-server-debug:
	. venv/bin/activate; PYTHONPATH=$(CURDIR)/src fastapi dev src/main.py

run-server-prod:
	. venv/bin/activate; PYTHONPATH=$(CURDIR)/src uvicorn main:app --port 8001

lock-requirements-from-fresh:
	rm -rf venv venv
	python -m venv venv
	. venv/bin/activate; pip install -r requirements/direct.txt
	. venv/bin/activate; pip freeze > requirements/locked.txt