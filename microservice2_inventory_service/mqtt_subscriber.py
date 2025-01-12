# import paho.mqtt.client as mqtt
# import json
# import requests
# from datetime import datetime
# import warnings

# warnings.filterwarnings("ignore", category=DeprecationWarning, message="Callback API version 1 is deprecated")

# # Configuration constants
# MQTT_BROKER = "mosquitto"
# MQTT_PORT = 1883
# MQTT_TOPIC = "orders"
# # INVENTORY_API_URL = "http://localhost:8000/update_inventory/"
# INVENTORY_API_URL = "http://host.docker.internal:8000/update_inventory/"

# class MQTTSubscriber:
#     def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT, topic=MQTT_TOPIC):
#         """
#         Initialize the MQTT Subscriber.
#         """
#         self.broker = broker
#         self.port = port
#         self.topic = topic

#         # Unique client ID for this subscriber
#         self.client = mqtt.Client(protocol=mqtt.MQTTv5)

#         # Attach event callbacks
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#         self.client.on_disconnect = self.on_disconnect

#     def on_connect(self, client, userdata, flags, reason_code,properties=None):
#         """
#         Handle successful connection to the MQTT broker.
#         """
#         if reason_code == 0:
#             print(f"[{datetime.now()}] Connected successfully to MQTT broker.")
#             print(f"Subscribing to topic: {self.topic}")
#             client.subscribe(self.topic, qos=1)
#         else:
#             print(f"[{datetime.now()}] Connection failed. Reason code: {reason_code}")

#     def on_message(self, client, userdata, message):
#         """
#         Handle incoming messages.
#         """
#         print("\n=== New Message Received ===")
#         print(f"Timestamp: {datetime.now()}")
#         print(f"Topic: {message.topic}")
#         print(f"QoS: {message.qos}")
#         print(f"Retain Flag: {message.retain}")

#         try:
#             # Decode the message payload
#             payload = message.payload.decode()
#             print("\nDecoded Payload (string):")
#             print(payload)

#             # Parse payload as JSON
#             order_data = json.loads(payload)
#             print("\nParsed JSON Data:")
#             print(json.dumps(order_data, indent=2))

#             # Process the parsed data (send to inventory API)
#             response = requests.post(INVENTORY_API_URL, json=order_data)
#             print(f"\nInventory Update Response: {response.status_code}")

#         except json.JSONDecodeError as e:
#             print(f"[Error] JSON decoding failed: {e}")
#         except requests.RequestException as e:
#             print(f"[Error] Failed to update inventory: {e}")
#         except Exception as e:
#             print(f"[Error] An unexpected error occurred: {e}")

#         print("=== End of Message ===\n")

#     def on_disconnect(self, client, userdata, reason_code):
#         """
#         Handle disconnection from the broker.
#         """
#         print(f"[{datetime.now()}] Disconnected from broker. Reason code: {reason_code}")

#     def start(self):
#         """
#         Start the MQTT subscriber.
#         """
#         try:
#             print(f"Connecting to MQTT broker at {self.broker}:{self.port}...")
#             self.client.connect(self.broker, self.port, keepalive=60)
#             print("Starting MQTT message loop...")
#             self.client.loop_forever()
#         except Exception as e:
#             print(f"[Error] Failed to start MQTT client: {e}")

# if __name__ == "__main__":
#     # Initialize and start the subscriber
#     subscriber = MQTTSubscriber()
#     subscriber.start()








import paho.mqtt.client as mqtt
import json
import requests
from datetime import datetime
import threading
import time
import warnings

# Ignore DeprecationWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning, message="Callback API version 1 is deprecated")

# Configuration constants
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "orders"
INVENTORY_API_URL = "http://host.docker.internal:8000/update_inventory/"

class MQTTSubscriber:
    def __init__(self, broker=MQTT_BROKER, port=MQTT_PORT, topic=MQTT_TOPIC):
        """
        Initialize the MQTT Subscriber.
        """
        self.broker = broker
        self.port = port
        self.topic = topic

        # Unique client ID for this subscriber
        self.client = mqtt.Client(protocol=mqtt.MQTTv5)

        # Attach event callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, reason_code, properties=None):
        """
        Handle successful connection to the MQTT broker.
        """
        if reason_code == 0:
            print(f"[{datetime.now()}] Connected successfully to MQTT broker.")
            print(f"Subscribing to topic: {self.topic}")
            client.subscribe(self.topic, qos=1)
        else:
            print(f"[{datetime.now()}] Connection failed. Reason code: {reason_code}")

    def on_message(self, client, userdata, message):
        """
        Handle incoming messages.
        """
        print("\n=== New Message Received ===")
        print(f"Timestamp: {datetime.now()}")
        print(f"Topic: {message.topic}")
        print(f"QoS: {message.qos}")
        print(f"Retain Flag: {message.retain}")

        try:
            # Decode the message payload
            payload = message.payload.decode()
            print("\nDecoded Payload (string):")
            print(payload)

            # Parse payload as JSON
            order_data = json.loads(payload)
            print("\nParsed JSON Data:")
            print(json.dumps(order_data, indent=2))

            # Process the parsed data (send to inventory API)
            response = requests.post(INVENTORY_API_URL, json=order_data)
            print(f"\nInventory Update Response: {response.status_code}")

        except json.JSONDecodeError as e:
            print(f"[Error] JSON decoding failed: {e}")
        except requests.RequestException as e:
            print(f"[Error] Failed to update inventory: {e}")
        except Exception as e:
            print(f"[Error] An unexpected error occurred: {e}")

        print("=== End of Message ===\n")

    def on_disconnect(self, client, userdata, reason_code):
        """
        Handle disconnection from the broker.
        """
        print(f"[{datetime.now()}] Disconnected from broker. Reason code: {reason_code}")

    def start(self):
        """
        Start the MQTT subscriber and listen for messages.
        """
        try:
            print(f"Connecting to MQTT broker at {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, keepalive=60)
            print("Starting MQTT message loop...")
            self.client.loop_start()  # Start the loop in a non-blocking way
        except Exception as e:
            print(f"[Error] Failed to start MQTT client: {e}")

def start_subscriber_in_background():
    """
    Start the MQTT subscriber in a separate thread to avoid blocking the main program.
    """
    subscriber = MQTTSubscriber()
    subscriber_thread = threading.Thread(target=subscriber.start)
    subscriber_thread.daemon = True  # Daemonize the thread, so it doesn't block the program
    subscriber_thread.start()

    print("MQTT Subscriber is running in the background...")

def main():
    # Start the MQTT subscriber in the background
    start_subscriber_in_background()

    # Simulate other activities (your Django app or other processes running here)
    try:
        while True:
            # Main program loop (e.g., Django app would be running here)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminating MQTT subscriber.")
        exit(0)

if __name__ == "__main__":
    main()














































