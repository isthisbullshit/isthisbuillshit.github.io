# GCP Infra

Pulumi project for the backend's GCP infrastructure.

## What it creates

- Artifact Registry Docker repository for backend images
- Cloud Storage bucket for backend event payloads
- Dedicated service account for the backend runtime
- Cloud Run service configured for the backend container
- Public invoker IAM binding for the Cloud Run service

## Required config

Set these before `pulumi up`:

```bash
cd infra
uv sync
mkdir -p .pulumi-state
./pulumi login file://$PWD/.pulumi-state
./pulumi stack init dev
./pulumi config set backendImage europe-docker.pkg.dev/isthisbullshit/isthisbullshit-backend/backend:latest
```

Optional overrides:

```bash
./pulumi config set gcp:region europe-west1
./pulumi config set bsDetectorUrl https://your-detector-service.run.app/
./pulumi config set --path allowedOrigins[0] https://isthisbullsh.it
./pulumi config set --path allowedOrigins[1] https://api.isthisbullsh.it
```

## Notes

- The default GCP project is `isthisbullshit`.
- The project-local Pulumi CLI is installed under `infra/.pulumi/` and launched via `./pulumi`.
- In this checkout, `.venv/bin/pulumi` can also point to the same local binary so `uv run pulumi ...` works when the symlink exists.
- The default workflow can be fully standalone by logging into the local filesystem backend at `file://$PWD/.pulumi-state` instead of Pulumi Cloud.
- The backend container must be built and pushed separately to the Artifact Registry repository output by this stack.
- The backend service receives `EVENTS_BUCKET_NAME`, `BS_DETECTOR_URL`, and `ALLOWED_ORIGINS` as environment variables.
