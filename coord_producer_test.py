#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script has as purpose to produce coordinates in intervals of
1 second, with the purpose of testing the system as a whole.

It should be run from the app's root directory.
"""
from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

from backend_iot.config import config, sr_config
from backend_iot.schema import gps_data_schema_str
from backend_iot.schemas_objects import GPSData, gpsdata_to_dict

from collections import defaultdict
import uuid
import random
import time
from datetime import datetime

def is_valid_uuid(uuid_str):
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def load_data(topics):
    base_file = 'tests/data/ruta'
    coords = defaultdict(list)
    for idx in range(1, len(topics) + 1):
        with open(f'{base_file}{idx}.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                coord = {
                    'uuid': topics[idx - 1],
                    'latitude': float(data[1]),
                    'longitude': float(data[0]),
                    'height': random.random(),
                    'velocity': random.random(),
                    'datetime': datetime.now().timestamp()
                }
                coords[topics[idx - 1]].append(coord)
    return coords


def delivery_response(err, event):
    if err is not None:
        print(f'Delivery failed on reading for {event.key().decode("utf8")}: {err}')
    else:
        print(f'Data delivered to {event.topic()}')


def produce_coords():
    producer = Producer(config)
    topics = producer.list_topics()
    topics_list = []
    for topic in topics.topics.keys():
        if is_valid_uuid(topic):
            topics_list.append(topic)

    coords = load_data(topics_list)
    schema_registry_client = SchemaRegistryClient(sr_config)
    json_serializer = JSONSerializer(gps_data_schema_str, schema_registry_client, gpsdata_to_dict)

    topics_idx = [0] * len(topics_list)
    while True:
        for idx in range(len(topics_list)):
            topic = topics_list[idx]
            data = coords[topic][topics_idx[idx]]
            topics_idx[idx] = (topics_idx[idx] + 1) % len(coords[topic])
            gps = GPSData(**data)
            producer.produce(
                topic=topic,
                key=str(time.time()),
                value=json_serializer(gps, SerializationContext(topic, MessageField.VALUE)),
                on_delivery=delivery_response
            )
        producer.flush()
        time.sleep(1)
        print('---')

if __name__ == "__main__":
    try:
        produce_coords()
    except KeyboardInterrupt:
        pass
    