from prefect import flow
from prefect.deployments import run_deployment


@flow
def orchestrate():
    run_deployment(name="extract/dev")
    run_deployment(name="transform-load/dev")
    run_deployment(name="cleanup/dev")


if __name__ == "__main__":
    orchestrate()
