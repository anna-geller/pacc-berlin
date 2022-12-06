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
