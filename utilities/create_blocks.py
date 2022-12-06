"""
https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
"""
from dotenv import load_dotenv
import os
from prefect.blocks.notifications import SlackWebhook
from prefect.filesystems import S3
from prefect_aws.credentials import AwsCredentials
from prefect_gitlab.credentials import GitLabCredentials
from prefect_gitlab.repositories import GitLabRepository

from utilities.deploy_utils import DEFAULT_BLOCK, save_block

load_dotenv()

gitlab_creds = GitLabCredentials(
    token=os.environ.get("GITLAB_ACCESS_TOKEN", DEFAULT_BLOCK)
)
save_block(gitlab_creds)

gitlab_repo = GitLabRepository(
    repository="https://gitlab.com/annageller/prefect.git",
    reference="main",
    credentials=gitlab_creds,
)
save_block(gitlab_repo)

slack = SlackWebhook(url=os.environ.get("SLACK_WEBHOOK_URL", DEFAULT_BLOCK))
save_block(slack)

aws = AwsCredentials(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", DEFAULT_BLOCK),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", DEFAULT_BLOCK),
    region_name="us-east-1",
)
save_block(aws)

s3 = S3(
    bucket_path=os.environ.get("AWS_S3_BUCKET_NAME", DEFAULT_BLOCK),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", DEFAULT_BLOCK),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", DEFAULT_BLOCK),
)
save_block(s3)
