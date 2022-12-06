from prefect import flow


@flow
def extract_data():
    return 42


@flow
def transform_data(x: int) -> int:
    return x * 2


@flow(log_prints=True, name="ETL with subflows")
def main():
    x = extract_data()
    y = transform_data(x)
    print(x)
    print(y)


if __name__ == "__main__":
    main()
