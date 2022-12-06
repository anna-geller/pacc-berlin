import asyncio
from prefect import get_client


async def main():
    async with get_client() as client:
        # set a concurrency limit of 10 on the 'small_instance' tag
        limit_id = await client.create_concurrency_limit(
            tag="small_instance", concurrency_limit=10
        )
        print(limit_id)


if __name__ == "__main__":
    asyncio.run(main())
