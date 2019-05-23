# This is a modified version of an example script found at this address, written by Google:
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iot/api-client/end_to_end_example/cloudiot_pubsub_example_mqtt_device.py

import datetime
import os
import time
from abc import ABC, abstractmethod
import jwt
import paho.mqtt.client as mqtt
import ssl
from constants import project_id, cloud_region, registry_id, algorithm

def create_jwt(project_id, private_key_file, algorithm):
    """Create a JWT (https://jwt.io) to establish an MQTT connection."""
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    print('Creating JWT using {} from private key file {}'.format(
        algorithm, private_key_file))
    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


class Device(ABC):
    """Represents the state of a single device."""

    def __init__(self, device_id, private_key_file, subfolder=None):
        self.connected = False
        self.mqtt_telemetry_topic = '/devices/{}/events'.format(device_id)

        if subfolder:
            self.mqtt_telemetry_topic += '/{}'.format(subfolder)

        client = mqtt.Client(
            client_id='projects/{}/locations/{}/registries/{}/devices/{}'.format(
                project_id,
                cloud_region,
                registry_id,
                device_id
            )
        )

        self.client = client

        client.username_pw_set(
            username='unused',
            password=create_jwt(
                project_id,
                private_key_file,
                algorithm))

        client.tls_set(ca_certs="roots.pem", tls_version=ssl.PROTOCOL_TLSv1_2)

        client.on_connect = self.on_connect
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect
        client.on_subscribe = self.on_subscribe
        client.on_message = self.on_message

        client.connect('mqtt.googleapis.com', 8883)

        client.loop_start()

        print("Hello from device {}".format(device_id))

        self.wait_for_connection(5)

        mqtt_config_topic = '/devices/{}/config'.format(device_id)

        client.subscribe(mqtt_config_topic, qos=1)


    def do_send_message(self, message):
        print('Publishing payload', message)
        self.client.publish(self.mqtt_telemetry_topic, message, qos=1)

    @abstractmethod
    def send_message(self):
        pass

    @abstractmethod
    def update_sensor_data(self):
        """This method will be called every second"""
        pass

    def wait_for_connection(self, timeout):
        """Wait for the device to become connected."""
        total_time = 0
        while not self.connected and total_time < timeout:
            time.sleep(1)
            total_time += 1

        if not self.connected:
            raise RuntimeError('Could not connect to MQTT bridge.')

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        """Callback for when a device connects."""
        if rc == 0:
            self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        """Callback for when a device disconnects."""
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        """Callback when the device receives a PUBACK from the MQTT bridge."""
        pass

    def on_subscribe(self, unused_client, unused_userdata, unused_mid,
                     granted_qos):
        """Callback when the device receives a SUBACK from the MQTT bridge."""
        if granted_qos[0] == 128:
            print('Subscription failed.')

    def on_message(self, unused_client, unused_userdata, message):
        """Callback when the device receives a message on a subscription."""
        payload = message.payload.decode('utf-8')
        print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))
