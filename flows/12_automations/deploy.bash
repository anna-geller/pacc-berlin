pip install git+https://github.com/PrefectHQ/prefect-aws.git@ecs-task-kill
pd build -n qa -q qa -ib ecs-task/qa -sb github/qa -a flows/healthcheck.py:healthcheck
pd build -n qa -q qa -ib ecs-task/qa -sb github/qa -a flows/bad.py:bad --skip-upload
prefect flow-run cancel cabf92ff-6769-4fc9-8eaf-b7ffb287e503