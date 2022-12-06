from prefect import task, flow, get_run_logger, allow_failure
import random


@task
def extract_data():
    return 42


@task
def extract_data_2():
    return 2


@task
def transform_data(x: int, y: int = 2) -> int:
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")
    else:
        return (x + 42) * y


@task
def clean_up_task():
    logger = get_run_logger()
    logger.info("Cleaning up 🧹")


@flow
def allow_flaky_transformation_to_pass():
    data = extract_data.submit()
    data_2 = extract_data_2.submit()
    result = transform_data.submit(data, data_2)
    clean_up_task.submit(wait_for=[allow_failure(result)])


if __name__ == "__main__":
    allow_flaky_transformation_to_pass()
