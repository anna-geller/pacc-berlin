from datetime import date
from prefect import flow
from prefect.deployments import run_deployment


@flow
def orchestrate(start_date: date = date(2022, 12, 1), end_date: date = date.today()):
    run_deployment(
        name="extract/dev", parameters=dict(start_date=start_date, end_date=end_date)
    )
    run_deployment(name="transform-load/dev")
    run_deployment(name="cleanup/dev")


if __name__ == "__main__":
    orchestrate()
