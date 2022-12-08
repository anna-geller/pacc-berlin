# `Parameter` validation

Flows can be called with both positional and keyword arguments. These arguments are resolved at runtime into a dictionary of **parameters** mapping name to value. These parameters are stored by the Prefect Orion orchestration engine on the flow run object. Type hints provide an easy way to enforce typing on your flow parameters via [pydantic](https://pydantic-docs.helpmanual.io/). This means *any* pydantic model used as a type hint within a flow will be coerced automatically into the relevant object type:

- Q: How to **disable** parameter `validation`?

  `@flow(validate_parameters=False)`

- Q: What happens when a flow is called with wrong parameter values? Does it move to a running state?

  No. If a flow run receives invalid parameters, it will move from a `Pending` state to a `Failed` without entering a `Running` state.

- Example: date validator

    ```python
    from prefect import flow
    from datetime import datetime
    
    @flow
    def what_day_is_it(date: datetime = None):
        if date is None:
            date = datetime.utcnow()
        print(f"It was {date.strftime('%A')} on {date}")
    
    if __name__ == "__main__":
        what_day_is_it("2022-12-07T12:00:00.180906")  # ok
        what_day_is_it("2022-42-07T12:00:00.180906")  # date: invalid datetime format, because month 42 doesn't exist!
    ```

- Example: dbt command **validator (within `valid list of values`)**

    ```python
    from prefect import flow, get_run_logger
    from pydantic import BaseModel, validator
    
    class DbtCommand(BaseModel):
        dbt_command: str
    
        @validator("dbt_command")
        def must_be_in(cls, dbt_cmd):
            valid_cmds = ["dbt run", "dbt test", "dbt docs", "dbt debug"]
            if dbt_cmd not in valid_cmds:
                raise ValueError("Invalid dbt command. Must be one of %s", valid_cmds)
            return dbt_cmd
    
    @flow
    def run_dbt_commands(dbt: DbtCommand):
        logger = get_run_logger()
        logger.info("Running dbt command: %s", dbt.dbt_command)
    
    if __name__ == "__main__":
        run_dbt_commands(dict(dbt_command="dbt debug"))
        print("------------------------")
        run_dbt_commands(dict(dbt_command="dbt run"))
        print("------------------------")
        run_dbt_commands(dict(dbt_command="dbt clean"))
        # deletes all folders specified in the clean-targets list specified in dbt_project.yml
    ```

- Example: dbt command **validator `startswith`**

    ```python
    from prefect import flow, get_run_logger
    from pydantic import BaseModel, validator
    
    class DbtCommand(BaseModel):
        dbt_command: str
    
        @validator("dbt_command")
        def must_be_in(cls, dbt_cmd):
            valid = "dbt run"
            if not dbt_cmd.startswith(valid):
                raise ValueError(f"Invalid dbt command. Must start with {valid}")
            return dbt_cmd
    
    @flow
    def dbt_run(dbt: DbtCommand):
        logger = get_run_logger()
        logger.info("Running dbt command: %s", dbt.dbt_command)
    
    if __name__ == "__main__":
        dbt_run(dict(dbt_command="dbt run"))
        print("------------------------")
        dbt_run(dict(dbt_command="dbt run my model"))
        print("------------------------")
        dbt_run(dict(dbt_command="dbt clean"))
        # deletes all folders specified in the clean-targets list specified in dbt_project.yml
    ```

- Example: str instead of `int` - **validating types**

    ```python
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
    ```