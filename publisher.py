import ssl
import time
import sounddevice
import wavio
import paho.mqtt.client as mqtt
from groq import Groq

GROQ_API_KEY = ""

HOST = ""
PORT = 8883

USER = ""
PASSWORD = ""

TOPIC = "mqtt/voiceCommands"

groq_client = Groq(api_key=GROQ_API_KEY)

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(USER, PASSWORD)
mqtt_client.tls_set(cert_reqs=ssl.CERT_REQUIRED)

mqtt_client.connect(HOST, PORT)

mqtt_client.loop_start()

print("Connected to MQTT broker...")

while True:
    print("Recording...")

    recording = sounddevice.rec(
        int(5 * 44100),
        samplerate=44100,
        channels=1,
        dtype="int16"
    )

    sounddevice.wait()

    wavio.write(
        "voice.wav",
        recording,
        44100,
        sampwidth=2
    )

    print("Recording finished.")

    with open("voice.wav", "rb") as audio_file:
        transcription = groq_client.audio.transcriptions.create(
            file=("voice.wav", audio_file.read()),
            model="whisper-large-v3-turbo"
        )

    command = transcription.text.strip()

    print("You said:", command)

    result = mqtt_client.publish(TOPIC, command)

    print("MQTT publish result:", result.rc)

    time.sleep(1)