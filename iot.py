import paho.mqtt.client as mqtt
import random
import json
import time
from web3 import Web3

def reconnect(client):
    attempts = 0
    while True:
        try:
            client.reconnect()
            print("Reconnected to MQTT broker")
            return
        except Exception as e:
            attempts += 1
            print(f"Reconnection attempt {attempts} failed: {e}")
            time.sleep(5)  # Wait before trying again

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))
    reconnect(client)

def generate_random_sensor_data():
    sensor_id = random.randint(1, 5)
    sensor_value = random.randint(0, 100)
    data = {
        "sensor_id": sensor_id,
        "moisture": sensor_value
    }
    return data


mqtt_ip = "mqtt.beia-telemetrie.ro"
mqtt_port = 1883
mqtt_topic = "/training/device/gabriel-comisaru/"

client = mqtt.Client()
client.on_disconnect = on_disconnect

client.connect(mqtt_ip, mqtt_port)
client.subscribe(mqtt_topic)

def main():
    try:
        client.loop_start()
        # Soil moisture sensor  
        while True:
            # generate random value
            soil_moisture = generate_random_sensor_data()
            payload = json.dumps(soil_moisture)
            client.publish(mqtt_topic, payload)
            print("Published: ", payload)
            time.sleep(60)

    except KeyboardInterrupt:
        print("Exiting...")
        client.disconnect()
        client.loop_stop()

if __name__ == "__main__":
    main()
