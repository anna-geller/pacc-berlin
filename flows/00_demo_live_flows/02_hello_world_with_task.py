from prefect import flow, task, get_run_logger


@task
def hello_world():
    logger = get_run_logger()
    logger.info("Hello from the workshop!")


@flow(log_prints=True)
def hi():
    print("Hi from Prefect, LiveEO! 🤗")
    hello_world()


if __name__ == "__main__":
    hi()