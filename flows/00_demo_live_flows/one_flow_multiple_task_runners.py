from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from prefect_ray.task_runners import RayTaskRunner


@task
def say_hello(name):
    print(f"hello {name}")


@task
def say_goodbye(name):
    print(f"goodbye {name}")


@flow(task_runner=RayTaskRunner())
def ray_greetings(names):
    for name in names:
        say_hello.submit(name)
        say_goodbye.submit(name)


@flow(task_runner=SequentialTaskRunner())
def greetings(names):
    for name in names:
        say_hello(name)
        say_goodbye(name)
    ray_greetings(names)


if __name__ == "__main__":
    greetings(["arthur", "trillian", "ford", "marvin"])
