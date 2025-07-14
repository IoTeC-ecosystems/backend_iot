from flask import (
    Blueprint, flash, g, redirect, request, url_for
)
from werkzeug.exceptions import abort

# Kafka imports
from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
import time

from .config import sr_config, config
from .schema import gps_data_schema_str
from .schemas_objects import GPSData, gpsdata_to_dict

bp = Blueprint('iot_data', __name__, url_prefix='/iot_data')

def delivery_response(err, event):
    if err is not None:
        print(f'Delivery failed on reading for {event.key().decode('utf8')}: {err}')
    else:
        print(f'Data deliverd to {event.topic()}')

def produce(data):
    """
    Produce data to kafka topic
    """
    topic = data['uuid']
    gps = GPSData(**data)
    schema_registry_client = SchemaRegistryClient(sr_config)
    json_serializer = JSONSerializer(gps_data_schema_str,
                                     schema_registry_client,
                                     gpsdata_to_dict)
    producer = Producer(config)
    producer.produce(topic=topic, key=gps.uuid,
                     value=json_serializer(gps, SerializationContext(topic, MessageField.VALUE)),
                     on_delivery=delivery_response)
    producer.flush()

@bp.route('/coordinates', methods=['POST'])
def coodinates():
    data = request.get_json()
    produce(data)
    return "Response"
