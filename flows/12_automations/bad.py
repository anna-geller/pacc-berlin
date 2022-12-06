from prefect import flow
import time


@flow
def bad():
    time.sleep(360)
    # raise ValueError("I fail and immediately end the run 🤒")


if __name__ == "__main__":
    bad()
