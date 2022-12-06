from datetime import timedelta
from prefect.tasks import task_input_hash
from prefect import task, flow
import time
from prefect.context import get_run_context


def cache_within_flow_run(context, parameters):
    id_ = context.task_run.flow_run_id
    key = f"{id_}-{task_input_hash(context, parameters)}"
    print(f"🔑Cache key: {key}")
    return key


@task(cache_key_fn=cache_within_flow_run, cache_expiration=timedelta(minutes=1), log_prints=True)
def expensive_computation() -> int:
    print("running an expensive operation")
    time.sleep(5)
    return 42


@flow(log_prints=True)
def cache_it():
    print(get_run_context().flow_run.id)
    for _ in range(5):
        expensive_computation()


if __name__ == "__main__":
    cache_it()
