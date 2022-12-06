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
