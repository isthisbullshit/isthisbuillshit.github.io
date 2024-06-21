.PHONY: run-server

install-server-locally:
	rm -rf venv venv
	python -m venv venv
	. venv/bin/activate; pip install -r requirements.locked.txt

run-server-debug:
	. venv/bin/activate; fastapi dev main.py

run-server-prod:
	-pkill gunicorn
	. venv/bin/activate; gunicorn main:app --workers 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080

pip-lock-from-fresh:
	rm -rf venv venv
	python -m venv venv
	. venv/bin/activate; pip install -r requirements.txt
	. venv/bin/activate; pip freeze > requirements.locked.txt