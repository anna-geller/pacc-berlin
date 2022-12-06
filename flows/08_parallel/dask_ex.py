from prefect import flow
from prefect_dask import DaskTaskRunner
from flows.parallel.tasks import extract, transform, load


@flow(task_runner=DaskTaskRunner())
def dask_flow():
    numbers = extract.submit()
    transformed_numbers = []
    for i in numbers.result():
        transformed_numbers.append(transform.submit(i))
    load.submit(numbers=transformed_numbers)


if __name__ == "__main__":
    dask_flow()
