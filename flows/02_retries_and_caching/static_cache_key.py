from datetime import timedelta
from prefect import flow, task
import time


def static_cache_key(context, parameters):
    return "static constant as a cache key"


@task(cache_key_fn=static_cache_key, cache_expiration=timedelta(seconds=20))
def cached_task():
    print("running an expensive operation")
    time.sleep(5)
    return 42


@flow(name="Static cache key flow", log_prints=True)
def main():
    cached_task()
    cached_task()
    cached_task()


if __name__ == "__main__":
    main()
