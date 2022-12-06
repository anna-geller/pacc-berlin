from prefect import flow, task


@task
def my_task():
    return 1


@flow
def my_flow():
    state = my_task.submit(return_state=True)
    return state.result() + 1


if __name__ == "__main__":
    flow_run_state = my_flow(return_state=True)
    assert flow_run_state.result() == 2
    # equivalent to:
    result = my_flow()
    assert result == 2
