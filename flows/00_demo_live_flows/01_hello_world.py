from prefect import flow


@flow(log_prints=True)
def hi():
    print("Hi from Prefect, LiveEO! 🤗")


if __name__ == "__main__":
    hi()
