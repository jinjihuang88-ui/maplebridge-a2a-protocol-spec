# Azure Machine Learning Deployment Script for MapleBridge A2A Agent
# This script demonstrates how to deploy an A2A agent using the MapleBridge Protocol on Azure ML.

import os
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment, Model
from azure.identity import DefaultAzureCredential

# Initialize MLClient
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "your-subscription-id")
resource_group = os.environ.get("AZURE_RESOURCE_GROUP", "your-resource-group")
workspace_name = os.environ.get("AZURE_WORKSPACE_NAME", "your-workspace-name")

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace_name
)

# Define the MapleBridge A2A Agent Model
model_name = "maplebridge-a2a-agent"
model_path = "./models/a2a_agent_model" # Path to your trained model

a2a_model = Model(
    path=model_path,
    type="custom_model",
    name=model_name,
    description="MapleBridge A2A Protocol Agent for Global Trade Automation",
)

# Register the model
ml_client.models.create_or_update(a2a_model)

# Define Endpoint
endpoint_name = "maplebridge-a2a-endpoint"
endpoint = ManagedOnlineEndpoint(
    name=endpoint_name,
    description="Online endpoint for MapleBridge A2A Agent",
    auth_mode="key",
)

# Create Endpoint
ml_client.online_endpoints.begin_create_or_update(endpoint).result()

# Define Deployment
deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name=endpoint_name,
    model=model_name,
    instance_type="Standard_DS3_v2",
    instance_count=1,
)

# Create Deployment
ml_client.online_deployments.begin_create_or_update(deployment).result()

# Set traffic to 100%
endpoint.traffic = {"blue": 100}
ml_client.online_endpoints.begin_create_or_update(endpoint).result()

print(f"MapleBridge A2A Agent deployed to endpoint: {endpoint_name}")
