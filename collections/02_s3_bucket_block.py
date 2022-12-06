"""
pip install s3fs
pip install prefect-aws
pip install aiobotocore==2.3.4
aws s3 ls s3://prefect-orion/demo/
unzip cats.zip
"""
from prefect.filesystems import S3

s3 = S3.load("default")
s3.put_directory("cats", "cats")

# in a flow:
# s3.get_directory(from_path="cats", local_path="cats_local")
