from prefect import task, flow


def business_logic():
    print("custom sensitive data")


@task(log_prints=False)
def my_task():
    print("print this only locally to the terminal")
    business_logic()


@flow(log_prints=True)
def my_flow():
    print("hello 👋")
    my_task()


if __name__ == "__main__":
    my_flow()
