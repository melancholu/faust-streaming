from datetime import datetime, timedelta

import logging
import faust
from environs import Env

logger = logging.getLogger(__name__)

env = Env()
env.read_env()

# constant
FAUST_APP_NAME = env.str("FAUST_APP_NAME")
BROKER_URL = env.str("FAUST_BROKER_URL")
TOPIC = env.str("TOPIC")

GROUP_TABLE_NAME = "group_table"
GROUP_TABLE_INTERVAL = env.int("GROUP_TABLE_INTERVAL")
GROUP_THRESHOLD = env.int("GROUP_THRESHOLD")

class User(faust.Record, serializer="json"):
    name: str
    address: str
    group: str

# app
app = faust.App(FAUST_APP_NAME, broker=BROKER_URL, consumer_auto_offset_reset="latest")

print(app)

# topic
handle_user = app.topic(TOPIC, value_type=User, partitions=1)

# table
group_table = app.Table(
    GROUP_TABLE_NAME, default=int, partitions=1
).tumbling(
    timedelta(minutes=GROUP_TABLE_INTERVAL),
    expires=timedelta(minutes=GROUP_TABLE_INTERVAL),
)

def handle_overflow(group):
    logger.info(f"group {group} is overflow")


@app.task
async def on_start():
    logger.info("on start")


@app.agent(handle_user, sink=[handle_overflow])
async def handle_user(users):
    async for user in users:
        logger.info(f'receive user {user}')
        group_table[user.group] += 1

        if group_table[user.group].now() > GROUP_THRESHOLD:
            yield group


if __name__ == "__main__":
    app.main()
