"""
aws s3 ls s3://prefect-orion/
"""
from prefect import flow
from prefect_aws import AwsCredentials
from prefect_aws.s3 import s3_download


@flow
def example_s3_download_flow():
    aws_credentials = AwsCredentials.load("default")
    key = s3_download(
        bucket="prefect-orion",
        key="docs/deployment_patterns.md",
        aws_credentials=aws_credentials,
    )
    print(key)


example_s3_download_flow()
