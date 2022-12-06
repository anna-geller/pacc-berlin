from prefect import flow


@flow
def extract_data():
    return 42


@flow
def transform_data(x: int) -> int:
    return x * 2


@flow(log_prints=True, name="Parent ETL flow with subflows")
def main():
    x = extract_data(return_state=True)
    y = transform_data(x, return_state=True)
    print(x.result())
    print(y.result())


if __name__ == "__main__":
    main()
