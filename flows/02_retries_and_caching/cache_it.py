from datetime import timedelta
from prefect.tasks import task_input_hash
from prefect import task, flow
import time


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=1))
def expensive_computation() -> int:
    time.sleep(5)
    return 42


@flow
def cache_it():
    expensive_computation()


if __name__ == "__main__":
    cache_it()
