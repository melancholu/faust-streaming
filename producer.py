import time
import random
import logging
import json
from confluent_kafka import Producer
from faker import Faker
from environs import Env

logger = logging.getLogger(__name__)

env = Env()
env.read_env()

BROKER_URL = env.str("PRODUCER_BROKER_URL")
TOPIC = env.str("TOPIC")

producer = Producer({'bootstrap.servers': BROKER_URL})
fake = Faker()

def make_msg():
    return {'name': fake.name(), 'address': fake.address(), 'group': random.randrange(1, 10)}

def run():
    while True:
        producer.produce(TOPIC, key='user', value=json.dumps(make_msg()))
        producer.poll(0)

        time.sleep(random.randrange(1, 10))

    producer.flush()

if __name__ == "__main__":
    run()
