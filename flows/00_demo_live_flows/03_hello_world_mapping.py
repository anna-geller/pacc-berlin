from prefect import flow, task
from typing import List


@task
def hello_world(user: str):
    print(f"✨ Hello from the workshop, {user}! 👋 📚")


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
):
    print("Hi from Prefect, LiveEO! 🤗")
    hello_world.map(users)


if __name__ == "__main__":
    hi()