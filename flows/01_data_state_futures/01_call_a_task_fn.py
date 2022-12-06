from prefect import task, flow


@task
def extract_data():
    return 42


@flow
def get_data():
    return 42


if __name__ == '__main__':
    nr = extract_data.fn()
    nr_2 = get_data.fn()
