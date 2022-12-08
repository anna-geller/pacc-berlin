from prefect import flow, task
from typing import List
import time


@task
def hello_world(user: str) -> None:
    print(f"✨ Hello from the workshop, {user}! 👋 📚")
    time.sleep(5)


@flow(log_prints=True)
def hi(
    users: List[str] = [
        "Marvin",
        "Anna",
        "Toby",
        "Rebecca",
        "Amelie",
        "Carlo",
        "Christian V.",
        "Christian R.",
        "Fernando",
        "Francesco",
        "Jorge",
        "Justin",
        "Laxmi",
        "Miguel",
        "Wieger",
        "Tobias",
    ]
) -> None:
    print("Hi from Prefect, LiveEO! 🤗")
    for user in users:
        # hello_world(user)  # would run sequentially + would be slow
        hello_world.with_options(name=user).submit(user)


if __name__ == "__main__":
    hi()
