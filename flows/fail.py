"""
prefect deployment build -n dev -q dev flows/fail.py:main -a
"""
from prefect import flow
import random


@flow(name="Manual retry")  # (retries=5, retry_delay_seconds=300, log_prints=True)
def main():
    print("Hi from Prefect! 🤗")
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")


if __name__ == '__main__':
    main()
