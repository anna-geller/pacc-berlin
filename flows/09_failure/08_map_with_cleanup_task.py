from prefect import flow, task, get_run_logger, allow_failure


@task
def extract():
    return [1, 2, 3]


@task
def add_one(x):
    if x == 2:
        raise Exception("Something is not right")
    return x + 1


@task
def add_two(x):
    return x + 2


@task
def cleanup_task():
    get_run_logger().info("Cleaning up e.g. removing temp Ray cluster")


@flow
def map_with_cleanup_task():
    a = extract()
    b = add_one.map(a)
    c = add_two.map(b)
    cleanup_task.submit(wait_for=[allow_failure(c)])


if __name__ == "__main__":
    map_with_cleanup_task()
