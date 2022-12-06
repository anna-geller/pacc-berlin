from prefect import flow


@flow
def extract_data():
    return 42


@flow(log_prints=True)
def get_data():
    x = extract_data()
    print(x)


if __name__ == '__main__':
    get_data()
