from prefect import flow, task
import random


@task
def my_task():
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")
    else:
        return 1


@flow(name="Get task run result only when it does NOT fail, no TR")
def main():
    state = my_task(return_state=True)
    maybe_result = state.result(raise_on_failure=False)
    if isinstance(maybe_result, ValueError):
        print("Oh no! The task failed. Falling back to '1'.")
        result = 1
    else:
        result = maybe_result

    return result + 1


flow_result = main()
assert flow_result == 2
