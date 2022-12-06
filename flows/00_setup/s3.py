from dotenv import load_dotenv
import os
from prefect.filesystems import S3


load_dotenv()


s3 = S3(
    bucket_path="prefect-orion/demo",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),  # when creating a block, you can pass this value from CI/CD Secrets
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),  # or retrieve those from environment variables
)
s3.save("demo", overwrite=True)
