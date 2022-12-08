## Data dependencies

- `future = task.submit()` - submit to task runner and return `PrefectFuture`
    - `future.wait()` will give you the **state** of a task run computation
    - `future.result()` will give you the return value, i.e. the **data**—when your task fails, the returned data is the exception message. Defalt is `future.result(raise_on_failure=True)` which means that failure will immediately stop the flow run (imagine the critical task that, if not completed, running anything else makes no sense)
    - `future.**result**(**raise_on_failure**=False)` will give you the return value, i.e. the **data, EVEN when your task fails**—when your task fails, the returned data is the exception message.
        - Without setting this to False, Prefect would **re-raise** that trapped exception
- `x = task.**submit**(**return_state**=True)` - submit to task runner and return `PrefectState`
    - `x.result()` - get data from state
    - `x.result(raise_on_failure=False)` -  get data even if the task fails

## State dependencies

- `future = task.submit()` - submit to task runner and return `PrefectFuture` - to pass that to downstream tasks to enforce `state dependencies`: use `task.submit(wait_for=[])`
    - `task.submit(wait_for=[one, two, three])`

## Example 1: fill in the blanks - submit to TR + get result

I want task my_task to be run on `ConcurrentTaskRunner` and return 2 as result.

```python
from prefect import flow, task

@task
def my_task():
    return 1

@flow
def my_flow():
    future = my_task.xxxxx()
    return future.xxxxx() + 1

if __name__ == '__main__':
    result = my_flow()
    assert result == 2
```

- Solution

    ```python
    from prefect import flow, task
    
    @task
    def my_task():
        return 1
    
    @flow
    def my_flow():
        future = my_task.submit()
        return future.result() + 1
    
    if __name__ == '__main__':
        result = my_flow()
        assert result == 2
    ```


## Example 2: fill in the blanks - sumit to TR, get state + get data from state

Submit a task to task runner, return a state object, get data (return value) from that state

```python
from prefect import flow, task

@task
def my_task():
    return 1

@flow
def my_flow():
    my_task_state = my_task.xxxxx(xxxxx)
    return my_task_state.xxxxx() + 1

if __name__ == '__main__':
    state = my_flow(xxxxx)
    assert state.xxxxx() == 2
    # equivalent to:
    result = my_flow()
    assert result == 2
```

- Solution

    ```python
    from prefect import flow, task
    
    @task
    def my_task():
        return 1
    
    @flow
    def my_flow():
        my_task_state = my_task.submit(return_state=True)
        return my_task_state.result() + 1
    
    if __name__ == "__main__":
        state = my_flow(return_state=True)
        assert state.result() == 2
        # equivalent to:
        result = my_flow()
        assert result == 2
    ```


## Example 3: fill in the blanks - sumit to TR, get state + get data from state only if it didn’t fail

Get task run result only when it does NOT fail

The debug log helps identify that task runner is used:

```python
prefect config set PREFECT_LOGGING_LEVEL='DEBUG'
```

```python
from prefect import flow, task
import random

@task
def my_task():
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")
    else:
        return 1

@flow(name="Get task run result only when it does NOT fail")
def main():
    state = xxxx # submit my_task to task runner and return state
    maybe_result = state.xxxxx(xxxxx)
    if isinstance(maybe_result, ValueError):
        print("Oh no! The task failed. Falling back to '1'.")
        result = 1
    else:
        result = maybe_result

    return result + 1

flow_result = main()
assert flow_result == 2
```

- Solution

    ```python
    from prefect import flow, task
    import random
    
    @task
    def my_task():
        if random.random() > 0.5:
            raise ValueError("Non-deterministic error has occured.")
        else:
            return 1
    
    @flow(name="Get task run result only when it does NOT fail")
    def main():
        state = my_task.submit(return_state=True)
        maybe_result = state.result(raise_on_failure=False)
        if isinstance(maybe_result, ValueError):
            print("Oh no! The task failed. Falling back to '1'.")
            result = 1
        else:
            result = maybe_result
    
        return result + 1
    
    flow_result = main()
    assert flow_result == 2
    ```

    ```python
    09:10:57.926 | INFO    | Flow run 'cerise-locust' - Created task run 'my_task-20c6ece6-0' for task 'my_task'
    09:10:57.927 | INFO    | Flow run 'cerise-locust' - Submitted task run 'my_task-20c6ece6-0' for execution.
    ```


## Example 4: fill in the blanks - do NOT sumit to TR, get state + get data from state only if it didn’t fail

The debug log helps identify that task runner is `not` used:

```python
prefect config set PREFECT_LOGGING_LEVEL='DEBUG'
```

```python
from prefect import flow, task
import random

@task
def my_task():
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")
    else:
        return 1

@flow(name="Get task run result only when it does NOT fail, no TR")
def main():
    state = my_task(xxxxx)
    maybe_result = state.xxxxx(xxxxx)
    if isinstance(maybe_result, ValueError):
        print("Oh no! The task failed. Falling back to '1'.")
        result = 1
    else:
        result = maybe_result

    return result + 1

flow_result = main()
assert flow_result == 2
```

- Solution

    ```python
    from prefect import flow, task
    import random
    
    @task
    def my_task():
        if random.random() > 0.5:
            raise ValueError("Non-deterministic error has occured.")
        else:
            return 1
    
    @flow(name="Get task run result only when it does NOT fail, no TR")
    def main():
        state = my_task(return_state=True)
        maybe_result = state.result(**raise_on_failure**=False)
        if isinstance(maybe_result, ValueError):
            print("Oh no! The task failed. Falling back to '1'.")
            result = 1
        else:
            result = maybe_result
    
        return result + 1
    
    flow_result = main()
    assert flow_result == 2
    ```

    ```python
    09:11:16.511 | INFO    | Flow run 'pompous-beluga' - Created task run 'my_task-20c6ece6-0' for task 'my_task'
    09:11:16.511 | INFO    | Flow run 'pompous-beluga' - Executing 'my_task-20c6ece6-0' immediately...
    ```


## Example 5: fill in the blanks - `state` dependencies when submitting tasks to a `ConcurrentTaskRunner` - tricky challenge ⚠️

Task 1, 2, 3, 5 must run concurrently

Task 4 requires 1, 2, 3 to be finished successfully before it can start

`clean_up_task` should run at the end

```python
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
    one = xxxxx
    two = xxxxx
    three = xxxxx
    four = task_4.xxxxx(xxxxx)
    five = task_5.xxxxx(xxxxx)
    clean_up_task.xxxxx(xxxxx)

if __name__ == "__main__":
    main()
```

- Solution

    ```python
    
    @flow(log_prints=True, name="Cleanup task may not get executed")
    def main():
        # 1, 2, 3 can run concurrently
        one = task_1.submit()
        two = task_2.submit()
        three = task_3.submit()
        four = task_4.submit(wait_for=[one, two, three])
        five = task_5.submit()
        clean_up_task.submit(wait_for=[four, five])
    ```

  - full solution

      ```python
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
      ```


## Example 6: fill in the blanks - state dependencies with cleanup task that allows failure

Same flow and tasks as before, but make sure that the cleanup task gets executed even if `four` and `five` fail:

```python
@flow(log_prints=True, name="Cleanup task may not get executed")
def main():
    # 1, 2, 3 can run concurrently
    one = task_1.submit()
    two = task_2.submit()
    three = task_3.submit()
    four = task_4.submit(wait_for=[one, two, three])
    five = task_5.submit()
    clean_up_task.submit(xxxxx)

if __name__ == "__main__":
    main()
```

- Solution

    ```python
    @flow(log_prints=True, name="Cleanup task may not get executed")
    def main():
        # 1, 2, 3 can run concurrently
        one = task_1.submit()
        two = task_2.submit()
        three = task_3.submit()
        four = task_4.submit(wait_for=[one, two, three])
        five = task_5.submit()
        clean_up_task.submit(wait_for=[**allow_failure**(four), **allow_failure**(five)])
    ```

  - full example

      ```python
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
          clean_up_task.submit(wait_for=[allow_failure(four), allow_failure(five)])
      
      if __name__ == "__main__":
          main()
      ```


## Example 7: fill in the blanks - data dependencies with cleanup task that allows failure

Tasks `extract_data` and `extract_data_2` can run concurrently

`transform_data` needs the return values of both tasks as input (data dependencies) → this transformation is flaky and fails 50% of the time (*e.g. transformation that fails when input data doesn’t adhere to the right format*)

`clean_up_task` should run at the end even if this transformation fails

```python
from prefect import task, flow, get_run_logger, allow_failure
import random

@task
def extract_data():
    return 42

@task
def extract_data_2():
    return 2

@task
def transform_data(x: int, y: int = 2) -> int:
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")
    else:
        return (x + 42) * y

@task
def clean_up_task():
    logger = get_run_logger()
    logger.info("Cleaning up 🧹")

@flow
def allow_flaky_transformation_to_pass():
    data = extract_data.xxxxx(xxxxx)
    data_2 = extract_data_2.xxxxx(xxxxx)
    result = transform_data.xxxxx(xxxxx)
    clean_up_task.submit(xxxxx)

if __name__ == "__main__":
    allow_flaky_transformation_to_pass()
```

- Solution

    ```python
    @flow
    def allow_flaky_transformation_to_pass():
        data = extract_data.submit()
        data_2 = extract_data_2.submit()
        result = transform_data.submit(data, data_2)
        clean_up_task.submit(wait_for=[allow_failure(result)])
    ```

- Full solution

    ```python
    from prefect import task, flow, get_run_logger, allow_failure
    import random
    
    @task
    def extract_data():
        return 42
    
    @task
    def extract_data_2():
        return 2
    
    @task
    def transform_data(x: int, y: int = 2) -> int:
        if random.random() > 0.5:
            raise ValueError("Non-deterministic error has occured.")
        else:
            return (x + 42) * y
    
    @task
    def clean_up_task():
        logger = get_run_logger()
        logger.info("Cleaning up 🧹")
    
    @flow
    def allow_flaky_transformation_to_pass():
        data = extract_data.submit()
        data_2 = extract_data_2.submit()
        result = transform_data.submit(data, data_2)
        clean_up_task.submit(wait_for=[allow_failure(result)])
    
    if __name__ == "__main__":
        allow_flaky_transformation_to_pass()
    ```