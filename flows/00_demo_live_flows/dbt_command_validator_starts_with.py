"""
pdb -a -n dev -q dev flows/06_parametrization/
"""
from prefect import flow, get_run_logger, task
from pydantic import BaseModel, validator


class ParameterValidator(BaseModel):
    dbt_command: str
    s3_path: str

    @validator("dbt_command")
    def must_be_in(cls, dbt_cmd):
        valid = "dbt run"
        if not dbt_cmd.startswith(valid):
            raise ValueError(f"Invalid dbt command. Must start with {valid}")
        return dbt_cmd

    @validator("s3_path")
    def s3_path_validator(cls, s3_path):
        valid = "s3://myvalidbucket/"
        if not s3_path.startswith(valid):
            raise ValueError(f"Invalid s3 path. Must start with {valid}")
        return s3_path


@task
def run_sth_critical(
    domain: str = "geospatial", lat: float = 52.5200, lon: float = 13.4050
):
    print(domain)
    print(lat)
    print(lon)


@flow(log_prints=True)
def main(
    myvalidbucket: ParameterValidator,
    domain: str = "geospatial",
    lat: float = 52.5200,
    lon: float = 13.4050,
):
    logger = get_run_logger()
    logger.info("Running dbt command: %s", myvalidbucket.dbt_command)
    logger.info("Using s3 path: %s", myvalidbucket.s3_path)
    run_sth_critical(domain, lat, lon)


if __name__ == "__main__":
    main(dict(dbt_command="dbt run", s3_path="s3://myvalidbucket/geospatial/berlin/"))
    print("------------------------")
    main(
        dict(dbt_command="dbt run my model", s3_path="s3://myvalidbucket/geospatial/hamburg/")
    )
    print("------------------------")
    main(dict(dbt_command="dbt clean", s3_path="s3://bad_bucket/"))
    main(dict(dbt_command="dbt run", s3_path="not_even_s3_path"))
