from dotenv import load_dotenv
import os
from prefect.blocks.notifications import SlackWebhook

load_dotenv()

slack = SlackWebhook(url=os.environ.get("SLACK_WEBHOOK_URL"))
slack.save("default", overwrite=True)
