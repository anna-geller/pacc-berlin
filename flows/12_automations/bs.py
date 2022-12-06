from faker import Faker
from platform import node, platform, python_version
import prefect
from prefect import flow, get_run_logger
from prefect.orion.api.server import ORION_API_VERSION as API


@flow
def bs():
    version = prefect.__version__
    say = Faker()
    logger = get_run_logger()
    logger.info("Network: %s. Instance: %s. Agent is healthy ✅️", node(), platform())
    logger.info("Python = %s. API: %s. Prefect = %s 🚀", python_version(), API, version)
    logger.info("We should %s 🧐", say.bs())


if __name__ == "__main__":
    bs()
