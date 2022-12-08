- use ConcurrentTaskRunner for IO operations
- the easiest is to use either `async` or `map` + `ConcurrentTaskRunner`, not both - even though technically it’s possible to combine both, it could get a little harder to understand and troubleshoot

## Example 1: async ETL

```python
import asyncio

from prefect import task, flow

@task(log_prints=True)
async def extract() -> list:
    return list(range(1, 11))

@task(log_prints=True)
async def transform(x: int) -> int:
    return x * 2

@task(log_prints=True)
async def load(x: int) -> None:
    print(f"final result {x}")

@flow(log_prints=True)
async def async_etl():
    nrs = await extract()
    for n in nrs:
        final = await transform(n)
        await load(final)

if __name__ == "__main__":
    asyncio.run(async_etl())
```

## Example 2: same ETL but submitted to `ConcurrentTaskRunner` with a `for` loop

already simpler, right?

```python
from prefect import task, flow

@task(log_prints=True)
def extract() -> list:
    return list(range(1, 11))

@task(log_prints=True)
def transform(x: int) -> int:
    return x * 2

@task(log_prints=True)
def load(x: int) -> None:
    print(f"final result {x}")

@flow(log_prints=True)
def async_etl():
    nrs = extract.submit()
    for n in nrs.result():
        final = transform.submit(n)
        load.submit(final)

if __name__ == "__main__":
    async_etl()
```

## Example 3: ETL with `ConcurrentTaskRunner`, and mapping (practical `TaskRunner` example)

again, even fewer lines + simpler syntax thanks to `.map()`

```python
from prefect import task, flow

@task(log_prints=True)
def extract() -> list:
    return list(range(1, 11))

@task(log_prints=True)
def transform(x: int) -> int:
    return x * 2

@task(log_prints=True)
def load(x: int) -> None:
    print(f"final result {x}")

@flow(log_prints=True)
def async_etl_map():
    nrs = extract.submit()
    final = transform.map(nrs)
    load.map(final)

if __name__ == "__main__":
    async_etl_map()
```

## Example 4: using `asyncio.gather()` - hard ⚠️

```python
import asyncio

from prefect import task, flow

@task(log_prints=True)
async def print_values(values):
    for value in values:
        await asyncio.sleep(1)  # yield
        print(value, end=" ")

@flow(log_prints=True)
async def async_flow():
    await print_values([1, 2])  # runs immediately
    coros = [print_values("abcd"), print_values("6789")]

    # asynchronously gather the tasks
    await asyncio.gather(*coros)

if __name__ == "__main__":
    asyncio.run(async_flow())
```

## Example 5: `async` + submitting to a `ConcurrentTaskRunner`

```python
import asyncio

from prefect import task, flow

@task(log_prints=True)
async def print_values(values):
    for value in values:
        await asyncio.sleep(1)  # yield
        print(value, end=" ")

@flow(log_prints=True)
async def async_flow():
    await print_values([1, 2])  # runs immediately
    await print_values.submit("abcd")
    await print_values.submit("6789")

if __name__ == "__main__":
    asyncio.run(async_flow())
```