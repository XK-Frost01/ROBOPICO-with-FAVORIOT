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

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
MQTT_HOST = "mqtt.favoriot.com"
MQTT_PORT = 1883  # Typically 1883 for non-SSL, 8883 for SSL
MQTT_DEVICE_DEVELOPER_ID = "YOUR_DEVICE_DEVELOPER_ID"
MQTT_DEVICE_ACCESS_TOKEN = "YOUR_DEVICE_ACCESS_TOKEN"  # device access token
MQTT_PUBLISH_TOPIC = "/v2/streams"
MQTT_RPC_TOPIC = "/v2/rpc"
MQTT_STATUS_TOPIC = "/v2/streams/status"

pool = socketpool.SocketPool(wifi.radio)    # Initialize socket pool
# Initialize MQTT client with a keep-alive interval of 60 seconds and loop timeout of 10 seconds
mqtt_client = MQTT.MQTT(
    broker=MQTT_HOST,
    port=MQTT_PORT,
    username=MQTT_DEVICE_ACCESS_TOKEN,
    password=MQTT_DEVICE_ACCESS_TOKEN,
    socket_pool=pool,
    keep_alive=60
)

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP16, echo_pin=board.GP17) # Ultrasonic sensor
ldr = analogio.AnalogIn(board.GP27) # LDR sensor
SA = analogio.AnalogIn(board.GP26)  # Line maker sensor
pixel = neopixel.NeoPixel(board.GP18, 2, auto_write=False)  # RGB LED
buzzer = pwmio.PWMOut(board.GP22, duty_cycle=0, frequency=440, variable_frequency=True) #buzzer

# DC motor setup
pwm_1a = pwmio.PWMOut(board.GP8, frequency=10000)
pwm_1b = pwmio.PWMOut(board.GP9, frequency=10000)
motorL = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(board.GP10, frequency=10000)
pwm_2b = pwmio.PWMOut(board.GP11, frequency=10000)
motorR = motor.DCMotor(pwm_2a, pwm_2b)

# Global variable for publish interval
publish_interval = 5  # Default to 10 seconds
obstacle = "False"
light = "False"
line = "False"
auto = "False"
RGB, color, r, g, b = 1,1,0,0,0

# Function to connect to WiFi
def connect_to_wifi():
    wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    print("Connected to WiFi!")
    print("IP address:", wifi.radio.ipv4_address)

# Define callback methods for MQTT events
def got_connected(client, userdata, flags, rc):
    print("Connected to MQTT broker!")
    print("Subscribing to topic...")
    client.subscribe((f"{MQTT_DEVICE_ACCESS_TOKEN}{MQTT_RPC_TOPIC}"), qos=2)
    print(f"Subscribed to {MQTT_DEVICE_ACCESS_TOKEN}{MQTT_RPC_TOPIC} with QoS 2")

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

def message(client, topic, msg):
    global publish_interval,line,auto
    global r,g,b,RGB

    print("======================================")
    print(f"New message on topic {topic}: {msg}")
    print("======================================")

    # Parse message and control the robot or update publish interval
    try:
        command = json.loads(msg)
        #=======================Mode======================
        if "publish_interval" in command:
            publish_interval = int(command["publish_interval"])
            print(f"Updated publish interval to {publish_interval} seconds")
        if "line" in command:
            line = command["line"]
            print(f"Updated line to {line}")
        if "auto" in command:
            auto = command["auto"]
        #===============Auto Control Direction============
        if auto == "True":
            print("Mode: AUTO")
        #==============Manual Control Direction===========
        if auto == "False":
            print("Mode: MANUAL")
        #==============RGB Control===========
        if "RGB" in command:
            RGB = int(command["RGB"])
        if "RGBRed" in command:
            r = int(command["RGBRed"])
        if "RGBGreen" in command:
            g = int(command["RGBGreen"])
        if "RGBBlue" in command:
            b = int(command["RGBBlue"])
        RGB_Show(RGB)
        #==============Buzzer Control===========
        if "buzzer" in command:
            if command["buzzer"] == "on":
                play_song()

    except json.JSONDecodeError:
        print("Failed to decode JSON message")

def RGB_Show(RGB):
    global r,g,b,color
    if color != RGB:
        r,g,b = 0,0,0
        color = RGB
    if RGB == 1:
        pixel[0] = (r,g,b)
    elif RGB == 2:
        pixel[1] = (r,g,b)
    pixel.show()

# Function to play a tone
def play_tone(frequency, duration):
    buzzer.frequency = frequency
    buzzer.duty_cycle = 65536 // 2  # 50% duty cycle
    time.sleep(duration)
    buzzer.duty_cycle = 0  # Turn off the buzzer after the duration

def play_song():
    play_tone(440,5)
    time.sleep(1)
    play_tone(None)

# Connect to WiFi
print("Connecting to WiFi...")
connect_to_wifi()

# Set up MQTT event handlers
mqtt_client.on_connect = got_connected
mqtt_client.on_disconnect = got_disconnected
mqtt_client.on_message = message

# Connect to the MQTT broker
print("Connecting to MQTT broker...")
mqtt_client.connect()

while True:
    try:
        print(f"[auto {auto}],[obstacle {obstacle}],[line {line}],[light {light}], [Interval {publish_interval}]")
    except Exception as e:
        print("Error:", e)
    # Check connection status and reconnect if necessary
    try_reconnect()
    # Process any incoming messages
    mqtt_client.loop(1)
