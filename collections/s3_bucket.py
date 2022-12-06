import asyncio
from prefect import flow, task, get_run_logger
from prefect_aws import AwsCredentials
from prefect_aws.s3 import S3Bucket


@task
async def upload_dir(s3_bucket: S3Bucket, local_path: str, bucket_path: str) -> None:
    logger = get_run_logger()
    files = await s3_bucket.put_directory(to_path=bucket_path, local_path=local_path)
    logger.info("Nr of files %s", files)


@task
async def download_dir(s3_bucket: S3Bucket, bucket_path: str, local_path: str) -> None:
    await s3_bucket.get_directory(from_path=bucket_path, local_path=local_path)


@flow
async def aws_s3_bucket() -> None:
    aws_creds = await AwsCredentials.load("default")
    s3_bucket = S3Bucket(
        bucket_name="prefect-orion",
        aws_credentials=aws_creds,
    )
    await upload_dir(s3_bucket, "docs", "docs2")
    await download_dir(s3_bucket, "docs2", "docs4")


if __name__ == "__main__":
    asyncio.run(aws_s3_bucket())
