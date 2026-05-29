from __future__ import annotations

import pulumi
import pulumi_gcp as gcp


config = pulumi.Config()
gcp_config = pulumi.Config("gcp")

project = gcp_config.require("project")
region = gcp_config.get("region") or "us-central1"

backend_service_name = config.get("backendServiceName") or "isthisbullshit-backend"
artifact_repository_id = config.get("artifactRepositoryId") or "isthisbullshit-backend"
artifact_repository_location = config.get("artifactRepositoryLocation") or "us"
bucket_location = config.get("bucketLocation") or "US"
bs_detector_url = config.get("bsDetectorUrl") or "http://localhost:8001/"
backend_image = config.require("backendImage")
allowed_origins = config.get_object("allowedOrigins") or [
    "https://isthisbullsh.it",
    "https://api.isthisbullsh.it",
]

required_services = [
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "storage.googleapis.com",
]

enabled_services = []
for api_name in required_services:
    enabled_services.append(
        gcp.projects.Service(
            api_name.replace(".", "-"),
            project=project,
            service=api_name,
            disable_on_destroy=False,
        )
    )

artifact_repository = gcp.artifactregistry.Repository(
    "backend-images",
    location=artifact_repository_location,
    repository_id=artifact_repository_id,
    description="Docker images for the isthisbullshit backend",
    format="DOCKER",
    opts=pulumi.ResourceOptions(depends_on=enabled_services),
)

events_bucket = gcp.storage.Bucket(
    "backend-events",
    name=f"{project}-{pulumi.get_stack()}-backend-events",
    location=bucket_location,
    uniform_bucket_level_access=True,
    force_destroy=False,
    opts=pulumi.ResourceOptions(depends_on=enabled_services),
)

runtime_service_account = gcp.serviceaccount.Account(
    "backend-runtime",
    account_id=f"{pulumi.get_stack()}-backend-runtime",
    display_name="Backend Cloud Run runtime",
)

gcp.storage.BucketIAMMember(
    "backend-events-writer",
    bucket=events_bucket.name,
    role="roles/storage.objectCreator",
    member=runtime_service_account.email.apply(lambda email: f"serviceAccount:{email}"),
)

cloud_run_service = gcp.cloudrunv2.Service(
    "backend",
    name=backend_service_name,
    location=region,
    ingress="INGRESS_TRAFFIC_ALL",
    template=gcp.cloudrunv2.ServiceTemplateArgs(
        service_account=runtime_service_account.email,
        containers=[
            gcp.cloudrunv2.ServiceTemplateContainerArgs(
                image=backend_image,
                ports=
                    gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080,
                    )
                ,
                envs=[
                    gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                        name="EVENTS_BUCKET_NAME",
                        value=events_bucket.name,
                    ),
                    gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                        name="BS_DETECTOR_URL",
                        value=bs_detector_url,
                    ),
                    gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                        name="ALLOWED_ORIGINS",
                        value=",".join(allowed_origins),
                    ),
                ],
                resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                    limits={
                        "cpu": "1",
                        "memory": "512Mi",
                    }
                ),
            )
        ],
    ),
    traffics=[
        gcp.cloudrunv2.ServiceTrafficArgs(
            percent=100,
            type="TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST",
        )
    ],
    opts=pulumi.ResourceOptions(depends_on=[artifact_repository, events_bucket]),
)

gcp.cloudrunv2.ServiceIamMember(
    "backend-invoker",
    name=cloud_run_service.name,
    location=cloud_run_service.location,
    role="roles/run.invoker",
    member="allUsers",
)

artifact_repository_url = pulumi.Output.concat(
    artifact_repository.location,
    "-docker.pkg.dev/",
    project,
    "/",
    artifact_repository.repository_id,
)

pulumi.export("project", project)
pulumi.export("region", region)
pulumi.export("artifactRepositoryId", artifact_repository.repository_id)
pulumi.export("artifactRepositoryUrl", artifact_repository_url)
pulumi.export(
    "suggestedBackendImage",
    pulumi.Output.concat(artifact_repository_url, "/backend:latest"),
)
pulumi.export("eventsBucketName", events_bucket.name)
pulumi.export("runtimeServiceAccountEmail", runtime_service_account.email)
pulumi.export("backendServiceName", cloud_run_service.name)
pulumi.export("backendUrl", cloud_run_service.uri)
