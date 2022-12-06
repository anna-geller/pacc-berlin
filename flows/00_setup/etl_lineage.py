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
    e = extract.submit()
    t = transform.submit(e)
    load.submit(t)


if __name__ == "__main__":
    etl()
