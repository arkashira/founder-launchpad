import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class DeploymentConfig:
    docker_container: str
    postgres_instance: str
    stripe_payment_gateway: Dict[str, str]

def deploy(config: DeploymentConfig) -> str:
    # Simulate provisioning of a Docker container on AWS Fargate
    docker_container_status = "provisioned"
    
    # Simulate provisioning of a PostgreSQL instance
    postgres_instance_status = "provisioned"
    
    # Simulate injection of environment variables for Stripe payment gateway
    stripe_payment_gateway_status = "injected"
    
    # Simulate deployment status
    deployment_status = "deploying"
    
    # Simulate live URL
    live_url = "https://example.com"
    
    return json.dumps({
        "docker_container_status": docker_container_status,
        "postgres_instance_status": postgres_instance_status,
        "stripe_payment_gateway_status": stripe_payment_gateway_status,
        "deployment_status": deployment_status,
        "live_url": live_url
    })

def get_deployment_status(deployment_config: DeploymentConfig) -> str:
    return deploy(deployment_config)
