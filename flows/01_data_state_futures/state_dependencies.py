from prefect import task, flow, allow_failure
import random


@task
def task_1():
    print("task 1 succeeded")


@task
def task_2():
    print("task 2 succeeded")


@task
def task_3():
    print("task 3 succeeded")


@task
def task_4():
    print("This task often fails")
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")
    else:
        print("task 4 succeeded")


@task
def task_5():
    print("task 5 succeeded")


@task
def clean_up_task():
    print("Cleaning up 🧹")


@flow(log_prints=True, name="Cleanup task may not get executed")
def main():
    # 1, 2, 3 can run concurrently
    one = task_1.submit()
    two = task_2.submit()
    three = task_3.submit()
    four = task_4.submit(wait_for=[one, two, three])
    five = task_5.submit()
    clean_up_task.submit(wait_for=[four, five])


if __name__ == "__main__":
    main()
