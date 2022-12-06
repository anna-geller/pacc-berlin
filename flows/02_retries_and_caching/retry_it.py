from prefect import flow
import random


@flow(retries=5, retry_delay_seconds=300, log_prints=True)
def retry_it():
    print("Hi from Prefect! 🤗")
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")


if __name__ == '__main__':
    retry_it()
