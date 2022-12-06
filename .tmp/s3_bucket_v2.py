import asyncio
from prefect import flow, task, get_run_logger
from prefect_aws import AwsCredentials
from prefect_aws.s3 import S3Bucket


@task
async def upload_dir(local_path: str, bucket_path: str) -> None:
    logger = get_run_logger()
    aws_creds = await AwsCredentials.load("default")
    s3_bucket = S3Bucket(
        bucket_name="prefect-orion",
        aws_credentials=aws_creds,
    )
    files = await s3_bucket.put_directory(to_path=bucket_path, local_path=local_path)
    logger.info("Nr of files %s", files)


@task
async def download_dir(bucket_path: str, local_path: str) -> None:
    aws_creds = await AwsCredentials.load("default")
    s3_bucket = S3Bucket(
        bucket_name="prefect-orion",
        aws_credentials=aws_creds,
    )
    await s3_bucket.get_directory(from_path=bucket_path, local_path=local_path)


@flow
async def aws_s3_bucket() -> None:
    await upload_dir("docs", "docs2")
    await download_dir("docs2", "docs3")


if __name__ == "__main__":
    asyncio.run(aws_s3_bucket())
