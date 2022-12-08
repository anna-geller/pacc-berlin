# Use `subflows` and `run_deployment` pattern to organize larger workflows

Two ways to orchestrate parent flows

- Simple parent flow with backfill

    ```python
    from datetime import date
    from prefect import flow
    import pandas as pd
    from prefect.deployments import run_deployment
    
    @flow(log_prints=True)
    def extract(start_date: date, end_date: date) -> pd.DataFrame:
        print(f"Running ingestion from {start_date} to {end_date}")
        return pd.DataFrame(data={"Users": ["Marvin", "LiveEO"]})
    
    @flow(log_prints=True)
    def transform_load():
        print(f"Got data: {df}")
    
    @flow(log_prints=True)
    def cleanup():
        print("Cleanup process")
    
    # parametrized for backfills
    @flow(log_prints=True)
    def parent(start_date: date = date(2022, 12, 1), end_date: date = date.today()):
        df = extract(start_date, end_date)
        run_deployment(name="transform-load/dev")
        cleanup()
    
    if __name__ == "__main__":
        parent()
    ```

- Failing parent flow with subflows

    ```python
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
    ```

- Simple parent flow from deployment

    ```python
    from prefect import flow
    from prefect.deployments import run_deployment
    
    @flow
    def orchestrate():
        run_deployment(name="extract/dev")
        run_deployment(name="transform-load/dev")
        run_deployment(name="cleanup/dev")
    
    if __name__ == "__main__":
        orchestrate()
    ```


## **Pros of subflows for data platform orchestration**

This subflow pattern is:

- **observable** — you can immediately see which child flows have been executed, and from there, you can navigate to individual tasks
- painless to **deploy** — there is `only one parent flow process` that needs to be deployed and **maintained** (*no moving parts that you would need to manage when orchestrating tens of different Kubernetes jobs for this process*)
- simple to **troubleshoot** — there’s only this one parent flow that runs on schedule and orchestrates your data platform — all you need is a notification when this process fails; the Prefect UI will tell you everything else you need to know for troubleshooting (*what failed, when, and why*)
- easy to **orchestrate** — `subflows` are `blocking`, which means that there is no additional orchestration (*dependency setting, waiting, or polling logic*) required to ensure that if the ingestion flow fails, the transformation flow shouldn’t start — this happens automatically when you leverage subflows (*to avoid that, add `return_state=True`*)

## **Cons of subflows (and how to overcome those)**

**Problem:**

- dependency management
- Using subflows running in a single flow run process may not work well if some of your flows (*e.g., those for ML or dbt transformations*) require `package` versions that conflict with those installed in your parent flow’s `infrastructure` environment.

**Solution:**

- keep using the parent flow approach, but trigger workflows that require different dependencies using the `run_deployment` pattern presented in the section below. This way, you can have the `best of both worlds`.

Another [problem](https://github.com/PrefectHQ/prefect/issues/7319) is that running subflows concurrently (while [possible](https://discourse.prefect.io/t/how-can-i-run-multiple-subflows-or-child-flows-in-parallel/96/10?u=anna_geller)) is not straightforward. There is an open issue to add `.submit()` **for subflows [here on GitHub](https://github.com/PrefectHQ/prefect/issues/6689) to make that process easier.

## **TL;DR of subflows**

This pattern can be best described with `simplicity`, [modularity](https://medium.com/the-prefect-blog/how-to-build-modular-dataflows-with-tasks-flows-and-subflows-in-prefect-5eaabdfbb70e), and ease of use at the cost of orchestration and infrastructure configurability. It’s particularly useful for largely standardized and `homogenous` deployment patterns, often maintained in a `monorepo`.

## **Orchestrating data platform with deployments**

The alternative to subflows is the `run_deployment` utility, which involves triggering flow runs from deployments. This pattern is especially helpful if you want `to run each flow within a separate container, Kubernetes pod, or other infrastructure`. It also helps coordinate work maintained by multiple teams without stepping on each other’s toes.

- Drawback: latency

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/aefaacea-d584-4da6-b452-e0bf3532b825/Untitled.png)

## **How to run deployments**

Here is a simple flow that demonstrates how you can apply that pattern to run the same flows using a different execution mechanism. Instead of running those directly in a parent flow run process, each subflow run is executed within its own deployment-specific infrastructure (*local process, docker container, Kubernetes job, or a serverless container*) e.g.

```python
from datetime import date
from prefect import flow
from prefect.deployments import run_deployment

@flow
def parent(
    start_date: date = date(2022, 11, 1),  # parametrized for backfills
    end_date: date = date.today(),
    deployment_name: str = "local-process",
):
    params = dict(start_date=start_date, end_date=end_date)
    run_deployment(
        name=f"raw-data-jaffle-shop/{deployment_name}",
        flow_run_name="raw-data-shop",
        parameters=params,
    )
    run_deployment(
        name=f"raw-data-marketing/{deployment_name}",
        flow_run_name="raw-data-marketing",
        parameters=params,
    )
    run_deployment(name=f"dbt-jaffle-shop/{deployment_name}", flow_run_name="shop")
    run_deployment(
        name=f"dbt-attribution/{deployment_name}", flow_run_name="attribution"
    )
    run_deployment(name=f"dashboards/{deployment_name}", flow_run_name="dashboards")
    run_deployment(name=f"sales-forecast/{deployment_name}", flow_run_name="forecast")

if __name__ == "__main__":
    parent()
```

This flow calls the `run_deployment` method for each respective flow’s deployment in the order you defined.

- Note

  All deployments from this example have been created by the [automated setup script in Part 3](https://medium.com/the-prefect-blog/modular-data-stack-build-a-data-platform-with-prefect-dbt-and-snowflake-part-3-7c325a8b63dc#9060) blog post recipe.

- Deployment build

    ```python
    prefect deployment build -n dev -q dev -a flows/11_parent_child/parent_child.py:extract
    prefect deployment build -n dev -q dev -a flows/11_parent_child/parent_child.py:transform_load
    prefect deployment build -n dev -q dev -a flows/11_parent_child/parent_child.py:cleanup
    ```

- Deployment parent flow

    ```python
    from prefect import flow
    from prefect.deployments import run_deployment
    
    @flow
    def orchestrate():
        run_deployment(name="extract/dev")
        run_deployment(name="transform-load/dev")
        run_deployment(name="cleanup/dev")
    
    if __name__ == "__main__":
        orchestrate()
    ```


## How does it work?

By default, the `run_deployment` method will:

- **Create** a (child) **flow run** for a given flow’s deployment
- **Poll** for its completion status, wait, and block further execution **until** this (child) flow run **finishes**

The parent flow orchestrates the next runs from deployments **only if the previous one succeeded** (*in the same way as subflows do*)

To change that default behavior, **disable polling** (*by adding `timeout=0*)`, which will result in **fire-and-forget** behavior.

<aside>
🛰️ If any child flow-run (*triggered from a deployment*) fails, the parent flow run will also be marked as failed.

</aside>

## ****Pros of running deployments****

1. Each child flow runs in its **own infrastructure** — this often makes it easier to manage execution environments and resources. You can use it to leverage a **separate Docker image**. It can also help **allocate a GPU** or a specific amount of **memory** to a given ML-specific **Kubernetes job**. This also allows you to orchestrate processes with complex, potentially non-Python, library dependencies.

2. Given that each component of this parent flow is a deployment, it can be **triggered** either from that parent flow or **independently**; for instance, you can trigger both the parent flow or only a single individual flow **from the UI** and the underlying execution metadata for that deployment is governed in one place.

3. The **fire-and-forget** method can be handy if you are interacting with some processes that don’t immediately affect your downstream work.

4. It allows setting **custom flow run names**.

## **Cons of running deployments**

**Problem:** Troubleshooting might be a little more challenging as you have more components to govern, and each child flow runs in its own process (*more moving parts*).

**Solution:** we are actively working on a feature called Automations that will allow you to observe the state of runs from any deployment and take an automated action on it (*such as triggering alerts or other flow runs and more*).

## TL;DR **of running deployments**

This pattern of [running **deployments](https://medium.com/the-prefect-blog/prefect-2-5-makes-modular-and-serverless-dataflows-easier-than-ever-44d65b625627)** can be best described with both the benefits and drawbacks of a decoupled per-flow-run infrastructure. It is particularly useful for heterogeneous deployment patterns and coordinating work developed by decentralized independent teams (*potentially in separate repositories*) or if your individual workflow components need to run in dedicated infrastructure.