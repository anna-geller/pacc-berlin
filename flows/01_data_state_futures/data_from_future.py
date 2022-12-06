from prefect import flow, task


@task
def my_task():
    return 1


@flow
def my_flow():
    future = my_task.submit()
    return future.result() + 1


if __name__ == '__main__':
    result = my_flow()
    assert result == 2
