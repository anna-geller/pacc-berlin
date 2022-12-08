# BEST PRACTICES 

## How to determine what should be a task?

- look at the `input` and `output` data that the workflow needs at each step
- look at how much `visibility` do you need
- if sth needs to run with a `task runner`, then it must be a `task`

## How to determine what should be a subflow?

- if the task seems to be doing too much = ideally a function should have `one responsibility`, if the task is doing too much, it's worth considering breaking it down into smaller tasks grouped into a subflow
- `logical grouping` of related components
- if you may want to execute it `independently`, from the UI
- input arguments to the functions → should they be `easy-to-change` and if so, do they need to be used as `Parameters`? parametrized flows are powerful and have `pydantic` `validation`

## Things to consider:

- `return` types and how they can be `serialized` when using results for `retries` or `caching` - by default, they must be serializable with cloudpickle
    - this means that you can’t return a DB connection or HTTP client such as boto3 client
- find the right balance between `flexibility` and `constraints` = some `standardization` is good for maintenance, but `too rigid` will make things harder to develop and lead to `conflicts`
- How is your team working with flows - maybe you can reuse some logic and run it as the same flow with multiple parametrized deployments

## AWS & Kubernetes & Docker:

- `AWS`: leverage `separate accounts` for dev/prod separation + Chrome account switcher extension = this way, you don't need to `hard code env details` in your code, you simply switch AWS accounts and Prefect workspaces
- don't use `latest` Docker image tag in prod and `default` K8s namespace
- How to install extra Code Dependencies (Prefect) at runtime? → you can use `EXTRA_PIP_PACKAGES` env var to install dependencies at runtime. `pip install ${EXTRA_PIP_PACKAGES}` is executed before the flow run starts.
    - However, Best Practices (Prefect) is to build a custom image for production use since downloading and installing packages during each flow run is `costly` and adds another risk for failure.
    - Use `EXTRA_PIP_PACKAGES` for development to iterate on dependencies without having to build image each time.
- `.dockerignore`
- `.gitignore`
- `.prefectignore`
- all those 3 can be aligned to some extent

# Deployment patterns: things to consider

Things to consider:

- `upload` & `--skip-upload` e.g. only upload the maintenance flow and skip the rest
- `.prefectignore` - best to extend it if you don’t want to upload everything to S3 - only your flow code + direct dependencies are needed → this can significantly speed up build times in CI/CD
- default for each agent is 10 sec → adjust to a different value when needed, especially if your agent doesn’t have lots of capacity

    ```bash
    prefect config set PREFECT_AGENT_QUERY_INTERVAL='20.0'
    ```

- generally a best practice to allocate enough **memory** and **CPU** to your **agent’s** container
- try to make CI/CD build process efficient - e.g.:
    - don’t rebuild Docker images unless needed (e.g. only when relevant dependencies changed, not when any code in the repo changes)
    - add caching to the build pipeline when required, esppecially when builds take too long

## Worth considering: `GitLabRepository` block for storage

- it may make your CI/CD a little **easier** since you don’t need to rebuild ECR images and pip packages only when your custom modules changed
- it may save some storage costs even - your code already lives on GitLab and Prefect needs to grab it from somewhere at runtime anywhere, so why not grab it from GitLab instead of S3
- *S3 would be valuable if your GitLab would be a monorepo, in which case building a CI/CD pipeline would be more challenging this way*
- Create PAT: [https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

```python
from prefect_gitlab.credentials import GitLabCredentials
from prefect_gitlab.repositories import GitLabRepository

gitlab_repo = GitLabRepository(
   repository="https://gitlab.com/annageller/prefect.git",
   reference="main",
   credentials=GitLabCredentials(token="GITLAB_ACCESS_TOKEN"))
gitlab_repo.save("default", overwrite=True)
```

- Full example of creating all blocks

    ```python
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
    ```