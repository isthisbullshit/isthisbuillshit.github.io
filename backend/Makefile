.PHONY: run-server

install-server-locally:
	rm -rf venv venv
	python -m venv venv
	. venv/bin/activate; pip install -r requirements.locked.txt

run-server-debug:
	. venv/bin/activate; fastapi dev main.py

run-server-prod:
	pkill gunicorn
	tmux new-session -d 'launchprod.sh'

pip-lock-from-fresh:
	rm -rf venv venv
	python -m venv venv
	. venv/bin/activate; pip install -r requirements.txt
	. venv/bin/activate; pip freeze > requirements.locked.txt