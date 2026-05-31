from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

import pulumi
import pulumi_gcp as gcp


@dataclass(frozen=True)
class KeycloakDeployment:
    service: gcp.cloudrunv2.Service
    runtime_service_account: gcp.serviceaccount.Account
    database_url: pulumi.Output[str]


def _postgres_url_to_jdbc(url: str) -> str:
    if url.startswith("jdbc:postgresql://"):
        return url

    parsed = urlsplit(url)
    if parsed.scheme not in {"postgres", "postgresql"}:
        return url

    query = dict(parse_qsl(parsed.query, keep_blank_values=True))

    if parsed.username:
        query.setdefault("user", parsed.username)
    if parsed.password:
        query.setdefault("password", parsed.password)

    hostname = parsed.hostname or ""
    if ":" in hostname and not hostname.startswith("["):
        hostname = f"[{hostname}]"

    netloc = hostname
    if parsed.port:
        netloc = f"{netloc}:{parsed.port}"

    jdbc_url = urlunsplit(
        (
            "jdbc:postgresql",
            netloc,
            parsed.path,
            urlencode(query, quote_via=quote),
            "",
        )
    )
    return jdbc_url


def deploy_keycloak(
    *,
    region: str,
    stack: str,
    depends_on: list[pulumi.Resource],
) -> KeycloakDeployment:
    config = pulumi.Config()

    service_name = config.get("keycloakServiceName") or "isthisbullshit-keycloak"
    image = config.require("keycloakImage")
    hostname = config.get("keycloakHostname")
    admin_username = config.get("keycloakAdminUsername") or "admin"
    admin_password = config.require_secret("keycloakAdminPassword")
    database_url = config.require_secret("keycloakDatabaseUrl").apply(
        _postgres_url_to_jdbc
    )
    min_instances = config.get_int("keycloakMinInstances")
    max_instances = config.get_int("keycloakMaxInstances") or 1

    runtime_service_account = gcp.serviceaccount.Account(
        "keycloak-runtime",
        account_id=f"{stack}-keycloak-runtime",
        display_name="Keycloak Cloud Run runtime",
        opts=pulumi.ResourceOptions(depends_on=depends_on),
    )

    envs: list[gcp.cloudrunv2.ServiceTemplateContainerEnvArgs] = [
        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
            name="KC_DB",
            value="postgres",
        ),
        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
            name="KC_DB_URL",
            value=database_url,
        ),
        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
            name="KC_BOOTSTRAP_ADMIN_USERNAME",
            value=admin_username,
        ),
        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
            name="KC_BOOTSTRAP_ADMIN_PASSWORD",
            value=admin_password,
        ),
        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
            name="KC_HTTP_ENABLED",
            value="true",
        ),
        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
            name="KC_PROXY_HEADERS",
            value="xforwarded",
        ),
        gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
            name="KC_HEALTH_ENABLED",
            value="true",
        ),
    ]

    if hostname:
        envs.append(
            gcp.cloudrunv2.ServiceTemplateContainerEnvArgs(
                name="KC_HOSTNAME",
                value=hostname,
            )
        )

    scaling = gcp.cloudrunv2.ServiceTemplateScalingArgs(
        max_instance_count=max_instances,
    )
    if min_instances is not None:
        scaling.min_instance_count = min_instances

    service = gcp.cloudrunv2.Service(
        "keycloak",
        name=service_name,
        location=region,
        ingress="INGRESS_TRAFFIC_ALL",
        template=gcp.cloudrunv2.ServiceTemplateArgs(
            service_account=runtime_service_account.email,
            scaling=scaling,
            containers=[
                gcp.cloudrunv2.ServiceTemplateContainerArgs(
                    image=image,
                    args=["start", "--optimized"],
                    ports=gcp.cloudrunv2.ServiceTemplateContainerPortsArgs(
                        container_port=8080,
                    ),
                    envs=envs,
                    resources=gcp.cloudrunv2.ServiceTemplateContainerResourcesArgs(
                        limits={
                            "cpu": "1",
                            "memory": "2Gi",
                        },
                        startup_cpu_boost=True,
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
        opts=pulumi.ResourceOptions(depends_on=depends_on),
    )

    gcp.cloudrunv2.ServiceIamMember(
        "keycloak-invoker",
        name=service.name,
        location=service.location,
        role="roles/run.invoker",
        member="allUsers",
    )

    pulumi.export("keycloakUrl", service.uri)
    pulumi.export("keycloakServiceName", service.name)
    pulumi.export("keycloakImage", image)
    pulumi.export("keycloakRuntimeServiceAccountEmail", runtime_service_account.email)

    return KeycloakDeployment(
        service=service,
        runtime_service_account=runtime_service_account,
        database_url=database_url,
    )
