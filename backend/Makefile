.PHONY: install-server-locally run-server-debug run-server-prod lock

install-server-locally:
	uv sync --locked

run-server-debug:
	uv run fastapi dev main.py

run-server-prod:
	uv run gunicorn main:app --workers 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080

lock:
	uv lock
