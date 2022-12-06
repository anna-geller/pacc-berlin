"""
prefect concurrency-limit create db 3
"""
import time
from prefect import task, flow


@task(log_prints=True, tags=["db"])
def db_task():
    print("using DB connection, need to mitigate DB pressure")
    time.sleep(10)


@flow
def db_flow():
    for i in range(1, 10):
        db_task.with_options(name=f"db_{i}").submit()


if __name__ == "__main__":
    db_flow()
