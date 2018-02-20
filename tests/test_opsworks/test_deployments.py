from __future__ import unicode_literals
import boto3
from freezegun import freeze_time
import sure  # noqa
import re

from moto import mock_opsworks


@freeze_time("2015-01-01")
@mock_opsworks
def test_create_deployment_response():
    client = boto3.client('opsworks', region_name='us-east-1')
    stack_id = client.create_stack(
        Name="test_stack_1",
        Region="us-east-1",
        ServiceRoleArn="service_arn",
        DefaultInstanceProfileArn="profile_arn"
    )['StackId']

    response = client.create_deployment(
        StackId=stack_id,
        Command={
            'Name': 'update_custom_cookbooks'
        }
    )

    response.should.contain("DeploymentId")


@freeze_time("2015-01-01")
@mock_opsworks
def test_describe_deployments():
    client = boto3.client('opsworks', region_name='us-east-1')
    stack_id = client.create_stack(
        Name="test_stack_1",
        Region="us-east-1",
        ServiceRoleArn="service_arn",
        DefaultInstanceProfileArn="profile_arn"
    )['StackId']
    deployment_id = client.create_deployment(
        StackId=stack_id,
        Command={
            'Name': 'update_custom_cookbooks'
        }
    )['DeploymentId']

    rv1 = client.describe_deployments(StackId=stack_id)
    rv2 = client.describe_deployments(DeploymentIds=[deployment_id])
    rv1['Deployments'].should.equal(rv2['Deployments'])

    rv1['Deployments'][0]['StackId'].should.equal(stack_id)
