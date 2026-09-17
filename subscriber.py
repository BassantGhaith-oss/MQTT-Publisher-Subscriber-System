import threading
import ssl
import webbrowser
import paho.mqtt.client as mqtt

HOST = ""
PORT = 8883

USER = ""
PASSWORD = ""

TOPIC = "mqtt/voiceCommands"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker...")
        client.subscribe(TOPIC)
        print("Subscribed to:", TOPIC)
    else:
        print("Connection failed:", rc)


def run_command(command):
    command = command.lower().strip().strip(".")

    print("Command:", command)

    if "open" in command and "youtube" in command:
        print("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif "open" in command and "google" in command:
        print("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif "open" in command and "linkedin" in command:
        print("Opening LinkedIn...")
        webbrowser.open("https://www.linkedin.com")

    else:
        print("Unknown command.")


def on_message(client, userdata, message):
    command = message.payload.decode("utf-8")
    run_command(command)


mqtt_client = mqtt.Client()

mqtt_client.username_pw_set(USER, PASSWORD)

mqtt_client.tls_set(
    cert_reqs=ssl.CERT_REQUIRED
)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print("Connecting to MQTT broker...")

mqtt_client.connect(HOST, PORT)

mqtt_thread = threading.Thread(
    target=mqtt_client.loop_forever,
    daemon=True
)

mqtt_thread.start()

print("MQTT subscriber is running...")
print("Waiting for voice commands...")

try:
    while True:
        input()

except KeyboardInterrupt:
    print("\nStopping subscriber...")
    mqtt_client.disconnect()
