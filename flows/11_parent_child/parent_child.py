"""
prefect deployment build -n dev -q dev -a flows/11_parent_child/parent_child.py:extract
prefect deployment build -n dev -q dev -a flows/11_parent_child/parent_child.py:transform_load
prefect deployment build -n dev -q dev -a flows/11_parent_child/parent_child.py:cleanup
"""
from datetime import date
from prefect import flow


@flow(log_prints=True)
def extract(start_date: date = date(2022, 12, 1), end_date: date = date.today()) -> int:
    print(f"Running ingestion from {start_date} to {end_date} ✅")
    return 42


@flow(log_prints=True)
def transform_load(x: int = 42) -> None:
    print(f"Got data: {x} 📊")


@flow(log_prints=True)
def cleanup() -> None:
    print("Cleanup process 🪣")


# parametrized for backfills
@flow(log_prints=True)
def parent(start_date: date = date(2022, 12, 1), end_date: date = date.today()) -> None:
    df = extract(start_date, end_date)
    transform_load(df)
    cleanup()


if __name__ == "__main__":
    parent()
