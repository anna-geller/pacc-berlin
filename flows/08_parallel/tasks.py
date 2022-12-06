import time
from prefect import task, get_run_logger


@task
def extract() -> list:
    logger = get_run_logger()
    nrs = [1, 2, 3, 4, 5, 6]
    logger.info("extracted nrs: %s", nrs)
    return nrs


@task
def transform(number: int) -> int:
    logger = get_run_logger()
    logger.info("transform %s", number)
    time.sleep(4)
    return number * 2


@task
def load(numbers: list) -> list:
    logger = get_run_logger()
    result = [i for i in numbers if i]
    logger.info("load result: %s", result)
    return result
