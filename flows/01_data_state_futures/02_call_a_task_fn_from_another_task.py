from prefect import task, flow


@task
def special_data():
    return 42


@task
def extract_data():
    return special_data.fn()


@flow(log_prints=True)
def get_data():
    x = extract_data()
    print(x)


if __name__ == "__main__":
    get_data()
