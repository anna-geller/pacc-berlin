from prefect import task, flow


@task(log_prints=True)
def extract() -> list:
    return list(range(1, 11))


@task(log_prints=True)
def transform(x: int) -> int:
    return x * 2


@task(log_prints=True)
def load(x: int) -> None:
    print(f"final result {x}")


@flow(log_prints=True)
def async_etl():
    nrs = extract.submit()
    for n in nrs.result():
        final = transform.submit(n)
        load.submit(final)


if __name__ == "__main__":
    async_etl()
