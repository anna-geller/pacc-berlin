
### Prefect future 🔮

**What is a `PrefectFuture`?**

**`PrefectFuture`** is an object that represents the result of a computation happening in a task runner. It simultaneously holds both:

1. The **data** returned by a task
2. The **state** of a (*potentially concurrent or parallel*) computation.

**What does it mean to return a `PrefectFuture`?** When you call tasks using `your_task.submit()`, they are submitted to a task runner, which creates a future for access to the state and result of a task.

Futures can be passed as data dependencies to downstream tasks, even when the task gets submitted for parallel execution to `Dask` or `Ray`, or concurrent execution with `async`:

- `future.wait()` will give you the **state** of a task run computation
- `future.result()` will give you the return value, i.e. the **data**—when your task fails, the returned data is the exception message.

![https://cdn-images-1.medium.com/max/1440/1*oj9iY9QYevWEtGg23CqxFg.png](https://cdn-images-1.medium.com/max/1440/1*oj9iY9QYevWEtGg23CqxFg.png)

Example showing how you can retrieve the state and return value from a `Prefect future`, even for failed tasks

---

### Blocking vs. non-blocking task calls

When running a flow that returns data directly, any task run that fails will **block** further execution and **stop the run immediately** (*the first flow in the image below*).

In contrast, when submitting your tasks for execution by a task runner, the blocking call (*returning a `PrefectFuture`*) allows you to run the entire flow with all tasks. The failure of one task doesn’t prevent the other task from executing (*the second flow in the image below*).

![https://cdn-images-1.medium.com/max/1440/1*2fisoYioZlr8ARAtoZ2jHQ.png](https://cdn-images-1.medium.com/max/1440/1*2fisoYioZlr8ARAtoZ2jHQ.png)

