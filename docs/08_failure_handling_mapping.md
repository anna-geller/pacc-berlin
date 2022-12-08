## Mapping with a task that fails

We take a **list** and **map over its elements**.

- **First** mapped chain will lead to Failed run for input `c`,
- **Second** mapped chain will lead to state `NotReady`, which indicates that `downstream_task` for **input `c` cannot even start**

```python
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
```

## Q: Mapping with a task that fails + add a cleanup task

In the current setup, the cleanup task requires all tasks from `c` to finish successfully before it can run:

```python
from prefect import flow, task, get_run_logger, allow_failure

@task
def extract():
    return [1, 2, 3]

@task
def add_one(x):
    if x == 2:
        raise Exception("Something is not right")
    return x + 1

@task
def add_two(x):
    return x + 2

@task
def cleanup_task():
    get_run_logger().info("Cleaning up e.g. removing temp Ray cluster")

@flow
def map_with_cleanup_task():
    a = extract()
    b = add_one.map(a)
    c = add_two.map(b)
    cleanup_task.submit(wait_for=[c])

if __name__ == "__main__":
    map_with_cleanup_task()
```

⚠️ **CHALLENGE for you:** Fix it by ensuring that `cleanup_task` will be executed **even if some upstream tasks from mapping steps failed**. How would you do that?

- Solution

  `allow_failure(c)`

    ```python
    @flow
    def map_with_cleanup_task():
        a = extract()
        b = add_one.map(a)
        c = add_two.map(b)
        cleanup_task.submit(wait_for=[allow_failure(c)])
    ```

- Full Solution code

    ```python
    from prefect import flow, task, get_run_logger, allow_failure
    
    @task
    def extract():
        return [1, 2, 3]
    
    @task
    def add_one(x):
        if x == 2:
            raise Exception("Something is not right")
        return x + 1
    
    @task
    def add_two(x):
        return x + 2
    
    @task
    def cleanup_task():
        get_run_logger().info("Cleaning up e.g. removing temp Ray cluster")
    
    @flow
    def map_with_cleanup_task():
        a = extract()
        b = add_one.map(a)
        c = add_two.map(b)
        cleanup_task.submit(wait_for=[allow_failure(c)])
    
    if __name__ == "__main__":
        map_with_cleanup_task()
    ```