import paho.mqtt.client as mqtt
import json

class MqttPublisher:
    def __init__(self, broker='mosquitto', port=1883, topic='orders'):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.broker, self.port)

    def publish(self, message):
        if isinstance(message, dict):
            message = json.dumps(message)
        self.client.publish(self.topic, message)

    def disconnect(self):
        self.client.disconnect()
