import time
import os
import board
import analogio
import adafruit_dht
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import json
import microcontroller
import pwmio
import neopixel
from adafruit_motor import motor
import adafruit_hcsr04

# WiFi credentials
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
MQTT_HOST = "mqtt.favoriot.com"
MQTT_PORT = 1883  # Typically 1883 for non-SSL, 8883 for SSL
MQTT_DEVICE_DEVELOPER_ID = "YOUR_DEVICE_DEVELOPER_ID"
MQTT_DEVICE_ACCESS_TOKEN = "YOUR_DEVICE_ACCESS_TOKEN"  # device access token
MQTT_PUBLISH_TOPIC = "/v2/streams"
MQTT_STATUS_TOPIC = "/v2/streams/status"
MQTT_CLIENTID = "@XK-PICO-ROBOPICO"

pool = socketpool.SocketPool(wifi.radio)# Initialize socket pool
# Initialize MQTT client with a keep-alive interval of 60 seconds and loop timeout of 10 seconds
mqtt_client = MQTT.MQTT(
    broker=MQTT_HOST,
    port=MQTT_PORT,
    username=MQTT_DEVICE_ACCESS_TOKEN,
    password=MQTT_DEVICE_ACCESS_TOKEN,
    socket_pool=pool,
    keep_alive=60
)

"""sensor pin - ultrasound, dht, ldr, line maker, air quality"""
ultrasound = adafruit_hcsr04.HCSR04(trigger_pin=board.GP16, echo_pin=board.GP17) # Ultrasonic sensor
dht = adafruit_dht.DHT11(board.GP5)                                       # Temperature,Humidity sensors
aq = analogio.AnalogIn(board.GP28)                                      # Air quality sensor
ldr = analogio.AnalogIn(board.GP27)                                              # LDR sensor
maker = analogio.AnalogIn(board.GP26)                                       # Line maker sensor
# Global variable for publish interval
publish_interval = 5 

# Function to connect to WiFi
def connect_to_wifi():
    wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Connected to WiFi!")
    print("IP address:", wifi.radio.ipv4_address)

# Define callback methods for MQTT events
def got_connected(client, userdata, flags, rc):
    print("Connected to MQTT broker!")
    print("Subscribing to topic...")
    client.subscribe(f"{MQTT_DEVICE_ACCESS_TOKEN}{MQTT_STATUS_TOPIC}")
    print(f"Subscribed to {MQTT_DEVICE_ACCESS_TOKEN}{MQTT_STATUS_TOPIC}")

def got_disconnected(client, userdata, rc):
    print("Disconnected from MQTT broker!")
    try_reconnect()

# Function to reconnect to WiFi and MQTT broker
def try_reconnect():
    try:
        if not wifi.radio.ipv4_address:
            connect_to_wifi()
        if not mqtt_client.is_connected():
            print("Reconnecting to MQTT broker...")
            mqtt_client.reconnect()
            print("Reconnected to MQTT broker")
    except Exception as e:
        print("Error during reconnection:", e)

def done_publish(client, userdata, topic, pid):
    print(f"Published to {topic} with PID {pid}")

def getData(client, topic, msg):
    print("======================================")
    print(f"New message on topic {topic}: {msg}")
    print("======================================")

#======================================Air Quality Sensor==================================
def read_voltage(air_analog_reading, max_adc_value=4095, max_voltage=3.3):
    return (air_analog_reading / max_adc_value) * max_voltage
def voltage_to_ppm(air_voltage_reading, baseline=1.3, slope=500):
    return max(0, (air_voltage_reading - baseline) / slope)
def classify_air_quality_ppm(ppm):# Classify air quality based on PPM
    if ppm > 1000:
        return "Hazardous"
    elif ppm > 500:
        return "Unhealthy"
    elif ppm > 100:
        return "Moderate"
    else:
        return "Good"

#====================================LDR Sensor==================================
def intensity(ldr_reading, min_voltage=0.0, max_voltage=3.3):
    global darkness
    # Map voltage to intensity percentage
    percentage = ((max_voltage - ldr_reading) / (max_voltage - min_voltage)) * 100
    percentage = max(0, min(100, percentage))  # Clamp to 0%-100%
    # Classify into intensity levels
    if percentage > 80:
        return "Bright"
    elif percentage > 50:
        return "Moderate"
    elif percentage > 20:
        return "Dim"
    else:
        darkness  = 'True'
        return "Dark"
    
def sendStreams():
    # Create JSON payload for Favoriot
    data = {
         "device_developer_id": MQTT_DEVICE_DEVELOPER_ID,  # Replace 'YOUR_DEVICE_ID' with your actual device ID
         "data":{
                "temperature": temperature,
                "humidity": humidity,
                "aq": aq.value,
                "aq_status": aq_status,
                "aq_volt": aq_volt,
                "air_quality_ppm": aq_ppm,
                "distance": Distance,
                "ldr": ldr_volt,
                "intensity": ldr,
                "line_vote": line_volt,                
                }
           }
            # Publish data to Favoriot MQTT broker with QoS 2
    mqtt_client.publish((f"{MQTT_DEVICE_ACCESS_TOKEN}{MQTT_PUBLISH_TOPIC}"), json.dumps(data))

# Connect to WiFi
print("Connecting to WiFi...")
connect_to_wifi()

# Set up MQTT event handlers
mqtt_client.on_connect = got_connected
mqtt_client.on_disconnect = got_disconnected
mqtt_client.on_publish = done_publish
mqtt_client.on_message = getData

# Connect to the MQTT broker
print("Connecting to MQTT broker...")
mqtt_client.connect()

# Variable to track the last publish time
last_publish_time = time.monotonic()

while True:
    try:
        current_time = time.monotonic()
        if current_time - last_publish_time >= publish_interval:
            temperature = dht.temperature
            humidity = dht.humidity
            Distance = ultrasound.distance
            line_volt = (maker.value * 3.3) / 4095
            ldr_volt = (ldr.value / 65535) * 3.3
            ldr = intensity(ldr_volt)
            aq_volt = read_voltage(aq.value)
            aq_ppm = voltage_to_ppm(aq_volt)
            aq_status = classify_air_quality_ppm(aq_ppm)
            sendStreams()
            last_publish_time = current_time
    except RuntimeError as error:
        # Errors happen fairly often with DHT sensors, just keep going
        print(error.args[0])
    except Exception as e:
        print("Error:", e)

    # Check connection status and reconnect if necessary
    try_reconnect()
    # Process any incoming messages
    mqtt_client.loop(1)