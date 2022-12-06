from prefect import task, flow


@task
def upstream_task(item):
    if item == "c":
        raise Exception("this upstream task failed")
    return str(item) + "+1"


@task
def downstream_task(item):
    return str(item) + "+2"


@flow
def demo():
    items = ["a", "b", "c", "d"]
    first = upstream_task.map(items)
    downstream_task.map(first)  # runs only for a, b, and d. c is in NotReady state


if __name__ == "__main__":
    demo()
