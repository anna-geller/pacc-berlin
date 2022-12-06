"""
return_state=True = this way, even if this child flow fails,
the parent flow will continue executing downstream tasks and flows
(e.g., to run some cleanup steps or important final processes
"""
from datetime import date
from prefect import flow
import pandas as pd
import random


@flow(log_prints=True)
def extract(start_date: date, end_date: date) -> pd.DataFrame:
    print(f"Running ingestion from {start_date} to {end_date}")
    return pd.DataFrame(data={"Users": ["Marvin", "LiveEO"]})


@flow(log_prints=True)
def transform_load(df):
    print(f"Got data: {df}")
    print("This step may fail...")
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")


@flow(log_prints=True)
def cleanup():
    print("Cleanup process")


# parametrized for backfills
@flow(log_prints=True)
def parent(start_date: date = date(2022, 12, 1), end_date: date = date.today()):
    df = extract(start_date, end_date)
    transform_load(df, return_state=True) # cleanup subflow will run
    # transform_load(df) # cleanup will never run
    cleanup()


if __name__ == "__main__":
    parent()