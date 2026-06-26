import json
from deploy import DeploymentConfig, get_deployment_status

def test_get_deployment_status():
    deployment_config = DeploymentConfig(
        docker_container="my-docker-container",
        postgres_instance="my-postgres-instance",
        stripe_payment_gateway={"stripe_key": "my-stripe-key", "stripe_secret": "my-stripe-secret"}
    )
    
    deployment_status = get_deployment_status(deployment_config)
    deployment_status_json = json.loads(deployment_status)
    
    assert deployment_status_json["docker_container_status"] == "provisioned"
    assert deployment_status_json["postgres_instance_status"] == "provisioned"
    assert deployment_status_json["stripe_payment_gateway_status"] == "injected"
    assert deployment_status_json["deployment_status"] == "deploying"
    assert deployment_status_json["live_url"] == "https://example.com"

def test_get_deployment_status_empty_config():
    deployment_config = DeploymentConfig(
        docker_container="",
        postgres_instance="",
        stripe_payment_gateway={}
    )
    
    deployment_status = get_deployment_status(deployment_config)
    deployment_status_json = json.loads(deployment_status)
    
    assert deployment_status_json["docker_container_status"] == "provisioned"
    assert deployment_status_json["postgres_instance_status"] == "provisioned"
    assert deployment_status_json["stripe_payment_gateway_status"] == "injected"
    assert deployment_status_json["deployment_status"] == "deploying"
    assert deployment_status_json["live_url"] == "https://example.com"
