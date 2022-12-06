"""
pip install s3fs
pip install aiobotocore==2.3.4
"""
from prefect.filesystems import S3

# from pathlib import Path
#
# x = Path(__file__).parent.joinpath("docs").expanduser().as_posix()
# print(x)

s3 = S3.load("default")
s3.put_directory(local_path="docs", to_path="docs2")
