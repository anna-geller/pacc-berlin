
### Return values

Any *flows* or *subflows* can return **data** and **states**. *Tasks* can additionally return **`PrefectFutures`** when they get submitted to a task runner.

### 1) Return data 📊

**What does it mean to return data?** This happens any time your flow or task directly returns any Python object. For instance, here is a flow returning an integer value:

```python
from prefect import flow


@flow
def reveal_the_answer() -> int:
    return 42
```

Prefect flow returning an integer value

And here is a dataflow where tasks and the main flow return pandas dataframes:

```python
from prefect import flow, task
import pandas as pd


@task
def get_dataframe() -> pd.DataFrame:
    return pd.DataFrame(data={"Users": ["Marvin", "You"]})


@task
def add_points(df: pd.DataFrame) -> pd.DataFrame:
    df["Karma_Points"] = [-42, 100]
    return df


@flow
def process_data() -> pd.DataFrame:
    df = get_dataframe()
    return add_points(df)


if __name__ == "__main__":
    result = process_data()
    print(result)
```

Flow and tasks returning Pandas dataframes

When you run this (*e.g., from your local terminal or a Jupyter notebook*), the result of your computation is a pandas dataframe:

![https://cdn-images-1.medium.com/max/1440/1*qslEUv1-VbDc5QRxP8h_uA.png](https://cdn-images-1.medium.com/max/1440/1*qslEUv1-VbDc5QRxP8h_uA.png)


**Returning data** (*rather than states or futures*) is the default behavior any time you call a task or flow. The returned values can be passed as data dependencies to any downstream tasks or even flows:

![https://cdn-images-1.medium.com/max/1440/1*9Ek_5rRdSdY2OYwSh46bhQ.png](https://cdn-images-1.medium.com/max/1440/1*9Ek_5rRdSdY2OYwSh46bhQ.png)


But you can also have a flow that returns nothing:

![https://cdn-images-1.medium.com/max/1440/1*jfuQp08sdGaS-g42clVyNQ.png](https://cdn-images-1.medium.com/max/1440/1*jfuQp08sdGaS-g42clVyNQ.png)


You can think of a Prefect flow code as plain Python with “extras” that you apply only when needed.

**Benefits of returning data:**

1. **Simplicity**—Prefect runs your flow directly in the flow run process.
2. **Readability**—your colleagues and collaborators don’t have to know anything about Prefect to understand this flow code—it’s just Python.
3. **Incremental adoption**—you can move your existing code to Prefect by adding a single flow decorator (*and optionally by [creating a deployment](https://medium.com/the-prefect-blog/declarative-dataflow-deployments-with-prefect-make-ci-cd-a-breeze-fe77bdbb58d4) from the CLI to schedule that flow*).