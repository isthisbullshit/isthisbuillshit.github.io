from __future__ import annotations

import pulumi
import pulumi_gcp as gcp

from keycloak import deploy_keycloak


config = pulumi.Config()
gcp_config = pulumi.Config("gcp")

project = gcp_config.require("project")
region = gcp_config.get("region") or "europe-west1"

stack = pulumi.get_stack()

github_owner = config.require("githubOwner")
github_repo = config.require("githubRepo")

backend_service_name = config.get("backendServiceName") or "isthisbullshit-backend"
artifact_repository_id = config.get("artifactRepositoryId") or "isthisbullshit-backend"
artifact_repository_location = config.get("artifactRepositoryLocation") or "europe"
bucket_location = config.get("bucketLocation") or "EU"
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
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
]

enabled_services = [
    gcp.projects.Service(
        api_name.replace(".", "-"),
        project=project,
        service=api_name,
        disable_on_destroy=False,
    )
    for api_name in required_services
]

project_info = gcp.organizations.get_project(project_id=project)
project_number = project_info.number


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
    name=f"{project}-{stack}-backend-events",
    location=bucket_location,
    uniform_bucket_level_access=True,
    force_destroy=False,
    opts=pulumi.ResourceOptions(depends_on=enabled_services),
)

runtime_service_account = gcp.serviceaccount.Account(
    "backend-runtime",
    account_id=f"{stack}-backend-runtime",
    display_name="Backend Cloud Run runtime",
    opts=pulumi.ResourceOptions(depends_on=enabled_services),
)

github_deployer_service_account = gcp.serviceaccount.Account(
    "github-deployer",
    account_id=f"{stack}-github-deployer",
    display_name="GitHub Actions deployer",
    opts=pulumi.ResourceOptions(depends_on=enabled_services),
)

gcp.storage.BucketIAMMember(
    "backend-events-writer",
    bucket=events_bucket.name,
    role="roles/storage.objectCreator",
    member=runtime_service_account.email.apply(lambda email: f"serviceAccount:{email}"),
)

# GitHub Actions deployer permissions

deployer_project_roles = [
    "roles/run.admin",
    "roles/artifactregistry.writer",
    "roles/iam.serviceAccountUser",
    "roles/storage.admin",
]

for role in deployer_project_roles:
    gcp.projects.IAMMember(
        f"github-deployer-{role.split('/')[-1]}",
        project=project,
        role=role,
        member=github_deployer_service_account.email.apply(
            lambda email: f"serviceAccount:{email}"
        ),
    )

# Workload Identity Federation for GitHub Actions

github_pool = gcp.iam.WorkloadIdentityPool(
    "github-pool",
    workload_identity_pool_id=f"{stack}-github-pool",
    display_name="GitHub Actions Pool",
    description="OIDC pool for GitHub Actions",
    disabled=False,
    opts=pulumi.ResourceOptions(depends_on=enabled_services),
)

github_provider = gcp.iam.WorkloadIdentityPoolProvider(
    "github-provider",
    workload_identity_pool_id=github_pool.workload_identity_pool_id,
    workload_identity_pool_provider_id="github-provider",
    display_name="GitHub Actions Provider",
    description="OIDC provider for GitHub Actions",
    disabled=False,
    attribute_mapping={
        "google.subject": "assertion.sub",
        "attribute.actor": "assertion.actor",
        "attribute.repository": "assertion.repository",
        "attribute.repository_owner": "assertion.repository_owner",
        "attribute.ref": "assertion.ref",
    },
    attribute_condition=(
        f"assertion.repository == '{github_owner}/{github_repo}'"
    ),
    oidc=gcp.iam.WorkloadIdentityPoolProviderOidcArgs(
        issuer_uri="https://token.actions.githubusercontent.com",
    ),
    opts=pulumi.ResourceOptions(depends_on=[github_pool]),
)

github_principal = pulumi.Output.concat(
    "principalSet://iam.googleapis.com/projects/",
    project_number,
    "/locations/global/workloadIdentityPools/",
    github_pool.workload_identity_pool_id,
    "/attribute.repository/",
    github_owner,
    "/",
    github_repo,
)

gcp.serviceaccount.IAMMember(
    "github-deployer-workload-identity-user",
    service_account_id=github_deployer_service_account.name,
    role="roles/iam.workloadIdentityUser",
    member=github_principal,
    opts=pulumi.ResourceOptions(depends_on=[github_provider]),
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
                ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                    container_port=8080,
                ),
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

deploy_keycloak(
    region=region,
    stack=stack,
    depends_on=[*enabled_services, artifact_repository],
)

github_workload_identity_provider = pulumi.Output.concat(
    "projects/",
    project_number,
    "/locations/global/workloadIdentityPools/",
    github_pool.workload_identity_pool_id,
    "/providers/",
    github_provider.workload_identity_pool_provider_id,
)

pulumi.export("cloudRunBackendUrl", cloud_run_service.uri)
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
pulumi.export("githubDeployerServiceAccountEmail", github_deployer_service_account.email)
pulumi.export("githubWorkloadIdentityProvider", github_workload_identity_provider)
pulumi.export("backendServiceName", cloud_run_service.name)
pulumi.export("backendUrl", cloud_run_service.uri)
