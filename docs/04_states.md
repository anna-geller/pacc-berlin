### Return state ✔️

**What is a `Prefect State`?** It’s an object that represents the state of a run. States are often called the “currency” of Prefect orchestration—they decide how your flow and task runs progress when they are scheduled, submitted, and eventually executed. There are states that represent retries, failures, completions, cancellations, crashes, and more.

Prefect allows you to take action when your tasks and flows transition into specific states and gives you control over how your automated dataflow reacts to the result of a computation. For instance, you may want to:

- get notified when your flow run **finishes** execution or when the underlying infrastructure **crashes**
- trigger some process any time someone **cancels** a flow run or when your tasks or flows are **retried**
- take action based on a specific type of **failure**.

All that is possible thanks to the rich vocabulary of Prefect states.

**What does it mean to return a `Prefect State` object?** Anytime you call your task with the `return_state=True` argument, Prefect will directly return a state object that you can use to build custom behavior based on a state change you care about, such as task or flow failing or retrying. Here are examples of how you can call that argument in both **tasks** and **subflows**:


```python
from prefect import flow, task, get_run_logger


@task
def add_one(x: int) -> int:
    return x + 1


@flow
def subflow_returning_data(emoji: str = "🚀") -> str:
    return f"Subflows are {emoji}!"


@flow
def basic_flow():
    logger = get_run_logger()
    state = add_one(41, return_state=True)  # returns Completed state
    data = state.result()  # get data from State object: 42
    also_data = add_one(41)  # returns data directly: 42
    logger.info("✅ State: %s.", state)
    logger.info("📊 Data: %s. Also data: %s", data, also_data)
    # the same works exactly the same way with subflows:
    state_of_a_subflow = subflow_returning_data("😎", return_state=True)
    subflow_data = state_of_a_subflow.result()
    also_subflow_data = subflow_returning_data("💙️")
    logger.info("✅️ Subflow state: %s.", state_of_a_subflow)
    logger.info(
        "📊 Subflow data: : %s. Also subflow data: %s",
        subflow_data,
        also_subflow_data,
    )


if __name__ == "__main__":
    basic_flow()
```


![https://cdn-images-1.medium.com/max/1440/1*1pGRQ6hdJvvImg3mqzTWXw.png](https://cdn-images-1.medium.com/max/1440/1*1pGRQ6hdJvvImg3mqzTWXw.png)

The above flow demonstrated how to return states when executing tasks and flows from a flow run process. 

Next, we'll look at task runners.

💡To learn more about Prefect states, check out [the following concept documentation](https://docs.prefect.io/concepts/states/).
