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
