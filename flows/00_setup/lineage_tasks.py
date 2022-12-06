from prefect import task, flow


@task
def extract() -> int:
    return 42


@task
def transform(x: int) -> int:
    return x * 2


@task
def load(x: int) -> None:
    print(x)


@flow(log_prints=True)
def etl():
    e = extract(return_state=True)
    t = transform(e, return_state=True)
    load(t, return_state=True)


if __name__ == "__main__":
    etl()
