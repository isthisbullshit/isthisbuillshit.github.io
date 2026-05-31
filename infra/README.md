# GCP Infra

Pulumi project for the backend's GCP infrastructure.

## What it creates

- Artifact Registry Docker repository for backend images
- Cloud Storage bucket for backend event payloads
- Dedicated service account for the backend runtime
- Cloud Run service configured for the backend container
- Cloud Run service configured for the Keycloak container
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
./pulumi config set --secret keycloakAdminPassword '<password>'
./pulumi config set --secret keycloakDatabaseUrl '<postgres-url>'
```

Optional overrides:

```bash
./pulumi config set bsDetectorUrl https://your-detector-service.run.app/
```

## Notes

- The default GCP project is `isthisbullshit`.
- The project-local Pulumi CLI is installed under `infra/.pulumi/` and launched via `./pulumi`.
- In this checkout, `.venv/bin/pulumi` can also point to the same local binary so `uv run pulumi ...` works when the symlink exists.
- The default workflow can be fully standalone by logging into the local filesystem backend at `file://$PWD/.pulumi-state` instead of Pulumi Cloud.
- The backend container must be built and pushed separately to the Artifact Registry repository output by this stack.
- The Keycloak container is built from `keycloak/Dockerfile`, pushed to the same Artifact Registry repository as the backend, and deployed by digest during `pulumi up`.
- The backend service receives `EVENTS_BUCKET_NAME`, `BS_DETECTOR_URL`, and `ALLOWED_ORIGINS` as environment variables.
