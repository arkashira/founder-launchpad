import pytest
from deploy import Deployer, Deployment

def test_deploy_success():
    deployer = Deployer()
    deployment = deployer.deploy("test_id")
    assert deployment.status == "success"
    assert deployment.url == "https://launchpad.axentx.com/test_id"
    assert deployment.logs == ["Deployment successful"]

def test_deploy_failure():
    deployer = Deployer()
    # Simulate an exception
    deployer.deploy = lambda id: Deployment(id, "failed", [f"Deployment failed: Test exception"])
    deployment = deployer.deploy("test_id")
    assert deployment.status == "failed"
    assert deployment.url is None
    assert deployment.logs == ["Deployment failed: Test exception"]

def test_get_status():
    deployer = Deployer()
    deployer.deploy("test_id")
    deployment = deployer.get_status("test_id")
    assert deployment.status == "success"
    assert deployment.url == "https://launchpad.axentx.com/test_id"
    assert deployment.logs == ["Deployment successful"]

def test_get_status_non_existent():
    deployer = Deployer()
    deployment = deployer.get_status("non_existent_id")
    assert deployment is None
