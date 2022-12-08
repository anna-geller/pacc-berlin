from prefect.deployments import run_deployment

run_deployment(
    "main/dev",
    flow_run_name="created from code from demo",
    parameters={
        "domain": "geospatial",
        "lat": 52.52,
        "lon": 13.405,
        "liveeo": {
            "dbt_command": "dbt run mymodel",
            "s3_path": "s3://myvalidbucket/berlin",
        },
    },
)
