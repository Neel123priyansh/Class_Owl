from twilio.rest import Client
import whisper
import requests
import time
import os

ESP32_URL = "http://<ESP32-IP>/capture"
OUTPUT_FILE = "audio.wav"
MODEL = whisper.load_model("base")

def capture_audio():
    os.system(f"arecord -D plughw:1,0 -f cd -d 10 {OUTPUT_FILE}")

def transcribe_audio():
    result = MODEL.transcribe(OUTPUT_FILE)
    return result['text']

def summarize(text):
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model":"llama3","prompt":f"Explain for a 12-year-old:\n{text}"}
    )
    return res.json()['response']

def send_whatsapp(text):
    client = Client("SID", "TOKEN")
    client.messages.create(
        from_="whatsapp:+14155238886",
        to="whatsapp:+919582794464",
        body=text
    )

print("⏳ ClassOwl Running...")

while True:
    capture_audio()
    full_text = transcribe_audio()
    summary = summarize(full_text)
    send_whatsapp(summary)
    print("📩 Summary sent to students!")
    time.sleep(60)
