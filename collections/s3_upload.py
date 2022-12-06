"""
aws s3 ls s3://prefect-orion/
"""
from prefect import flow
from prefect_aws import AwsCredentials
from prefect_aws.s3 import s3_upload


@flow
def example_s3_upload_flow():
    aws_credentials = AwsCredentials.load("default")
    with open("images/speed.png", "rb") as file:
        key = s3_upload(
            bucket="prefect-orion",
            key="speed.png",
            data=file.read(),
            aws_credentials=aws_credentials,
        )
        print(key)


example_s3_upload_flow()
