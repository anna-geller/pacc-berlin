from prefect import task, flow, pause_flow_run
from prefect import get_run_logger
from prefect.context import get_run_context
from prefect.blocks.notifications import SlackWebhook
from prefect.settings import PREFECT_UI_URL


def get_ui_flowrun_url() -> str:
    id_ = get_run_context().flow_run.dict().get('id')
    ui_url = PREFECT_UI_URL.value() or "http://ephemeral-orion/api"
    return f"{ui_url}/flow-runs/flow-run/{id_}"


def send_alert(message: str):
    slack_webhook_block = SlackWebhook.load("default")
    slack_webhook_block.notify(message)


@task
def run_initial_processing():
    logger = get_run_logger()
    logger.info("Processing something important 🤖")
    logger.info("Calculating the answer to life, the universe, and everything...")


@task
def run_something_critical():
    logger = get_run_logger()
    logger.info("We'll reveal the answer to life, the universe, and everything!")
    logger.info("The answer is... 42!")


@flow
def semi_manual_process(
        process: str = "ChatGPT training",
) -> None:
    logger = get_run_logger()
    run_initial_processing()
    url = get_ui_flowrun_url()
    send_alert(f"{process} finished. Please approve to continue processing: {url}")
    logger.info("Waiting for approval...")
    pause_flow_run(timeout=600) 
    logger.info("Process got approved! 🎉 Moving on to the next task")
    run_something_critical()  # post-processing, ML training process, reporting on KPIs


if __name__ == "__main__":
    semi_manual_process()