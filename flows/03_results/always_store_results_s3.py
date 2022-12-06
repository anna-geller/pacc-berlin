"""
aws s3 ls s3://prefect-orion/dev/
prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT = "true"
"""
from prefect import flow


@flow(persist_result=True, result_storage="s3/dev")
def always_store_results():
    return "Hi from Results! 👋"


if __name__ == "__main__":
    always_store_results()
