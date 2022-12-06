from prefect import flow
from datetime import datetime


@flow
def what_day_is_it(date: datetime = None):
    if date is None:
        date = datetime.utcnow()
    print(f"It was {date.strftime('%A')} on {date}")


if __name__ == "__main__":
    what_day_is_it("2022-12-07T12:00:00.180906")  # ok
    what_day_is_it("2022-42-07T12:00:00.180906")  # date: invalid datetime format
