"""
any pydantic model used as a type hint within a flow will be coerced automatically into the relevant object type
- parameter values can be provided to a flow via API using a deployment
- flow run parameters sent to the API on flow calls are coerced to a serializable form.
- type hints on your flow functions provide you a way of automatically coercing JSON provided values
to their appropriate Python representation.
"""
from prefect import flow, get_run_logger
from pydantic import BaseModel


class Model(BaseModel):
    a: int
    b: float
    c: str


@flow
def model_validator(model: Model):
    logger = get_run_logger()
    logger.info(model)


if __name__ == "__main__":
    # model_validator(model=dict(a=42, b=4.2, c="Marvin"))
    # equivalent to - but this should intentionally fail:
    model_validator(model={"a": "Not an int", "b": 4.2, "c": "Marvin"})
