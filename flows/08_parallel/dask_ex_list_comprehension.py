from prefect import flow
from prefect_dask import DaskTaskRunner
from flows.parallel.tasks import extract, transform, load


@flow(task_runner=DaskTaskRunner())
def dask_flow_list_comprehension():
    numbers = extract.submit()
    transformed_numbers = [transform.submit(i) for i in numbers.result()]
    load.submit(numbers=transformed_numbers)


if __name__ == "__main__":
    dask_flow_list_comprehension()
