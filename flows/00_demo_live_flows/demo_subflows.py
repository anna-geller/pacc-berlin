from prefect import task, flow


@flow
def extract_data():
    return 42


@flow
def extract_sth_esle():
    return 24


@flow(log_prints=True)
def get_data():
    x = extract_data()
    y = extract_sth_esle()
    print(x)
    print(y)


if __name__ == "__main__":
    get_data()
