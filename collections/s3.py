"""
pip install s3fs
pip install prefect-aws
pip install aiobotocore==2.3.4
aws s3 ls s3://prefect-orion/dev/
"""
from prefect.filesystems import S3

s3 = S3.load("default")
s3.put_directory(local_path="docs", to_path="docs")
s3.get_directory(from_path="docs", local_path="docs2")
