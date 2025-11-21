# 🦉 ClassOwl – AI‑Powered Classroom Assistant

ClassOwl is an intelligent classroom companion built using **Raspberry Pi + Local LLM (Ollama)** that listens to real classroom teaching, converts it into simplified multilingual notes, and automatically sends them to students via **WhatsApp**. The system also includes an AI chatbot that answers doubts based on captured audio and classroom content.

![alt text](https://github.com/Neel123priyansh/Class_Owl/blob/main/img/Screenshot%202025-11-21%20203822.png/?raw=true)
---

## 🚀 Features

* 🎙️ **Real‑time speech‑to‑text transcription** using Whisper
* 🔤 **Summarization and simplification** using Ollama LLM
* 🌎 **Translation into regional languages** (Hindi, Tamil, Telugu, Bengali, Marathi, etc.)
* 📸 **Classboard monitoring using ESP32‑CAM**
* 💬 **WhatsApp delivery of notes to students**
* ❓ **AI chatbot for clearing doubts based on lecture content**
* 🖥️ OLED display for live system status

---

## 🧠 System Architecture

```
ESP32‑CAM  →  Raspberry Pi → Whisper ASR → LLM (Ollama) → WhatsApp API → Students
                      ↓
                OLED feedback
```

---

## 🛠️ Hardware Requirements

| Component                | Purpose                              |
| ------------------------ | ------------------------------------ |
| Raspberry Pi 4 (4GB/8GB) | Main processor + LLM execution       |
| ESP32‑CAM                | Capture classroom blackboard/visuals |
| USB Microphone           | Audio capture                        |
| SSD1306 OLED Display     | Live status output                   |
| USB‑TTL Converter        | Flash ESP32‑CAM Firmware             |
| 5V Power Supply (3–4A)   | Stable power for Pi & camera         |

---

## 🔧 Software Requirements

| Component           | Version                  |
| ------------------- | ------------------------ |
| Raspberry Pi OS     | Latest                   |
| Python 3.10+        | Programming & control    |
| Ollama              | Local LLM engine         |
| Whisper             | Speech to text           |
| Twilio WhatsApp API | Messaging service        |
| OpenCV (optional)   | Camera stream processing |

![alt text](https://github.com/Neel123priyansh/Class_Owl/blob/main/img/Screenshot%202025-01-23%20152429.png/?raw=true)

---

## 📦 Installation

### 1. Update Raspberry Pi

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Dependencies

```bash
sudo apt install python3-pip i2c-tools ffmpeg -y
pip3 install openai-whisper twilio requests Adafruit-SSD1306 pillow
```

### 3. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3
```

---

## 🔌 Circuit Wiring Summary

| Raspberry Pi Pin | Device              |
| ---------------- | ------------------- |
| Pin 1 (3.3V)     | SSD1306 VCC         |
| Pin 3 (SDA)      | SSD1306 SDA         |
| Pin 5 (SCL)      | SSD1306 SCL         |
| Pin 6 (GND)      | SSD1306 & ESP32 GND |
| Pin 2/4 (5V)     | ESP32‑CAM Power     |

> Important: All modules must share a **common ground**.

---

## 🧪 Chatbot
![alt text](https://github.com/Neel123priyansh/Class_Owl/blob/main/img/Screenshot%202025-01-18%20185847.png/?raw=true)

---

## 🎦 ESP32‑CAM Setup

Flash ESP32‑CAM with Arduino IDE sketch included in repository.
After flashing, access stream via:

```
http://<ESP-IP>/stream
```

---

## 🧩 Core Pipeline Script

Run main automation script:

```bash
python3 classowl_main.py
```

The script:

* Records audio
* Transcribes using Whisper
* Summarizes with Ollama
* Sends final notes to students via WhatsApp

---

## 💬 LLM working on backend to summerize the video 
Video_Link: https://github.com/Neel123priyansh/Class_Owl/blob/main/img/Baba.mp4

---

## 📚 Output Formats

* Bullet‑point notes
* Revision summary
* MCQ quiz
* Board exam style answers
* Multilingual version

---

## 🧭 Roadmap

* [ ] Add teacher‑voice profile tuning
* [ ] Generate mind‑maps
* [ ] Live question answering during class
* [ ] Student performance analytics dashboard

---

---

## 🦉 OLED Display Interaction Behavior

The ClassOwl includes a small OLED display that behaves like an animated owl to provide visual feedback in real-time.

### 🟢 Active Recording / Processing Mode

* The owl **eyes remain open and blinking**.
* A small mic or camera icon appears to indicate **live capture**.
* Status text like:

  * `Listening...`
  * `Analyzing...`
  * `Summarizing lesson...`
![alt text](https://github.com/Neel123priyansh/Class_Owl/blob/main/img/IMG-20250919-WA0021.jpg/?raw=true)

### 🟡 Idle Mode

* The owl's eyes **half-close**, resembling a resting state.
* A subtle **breathing animation** keeps it visually alive.
* Text displayed: `Standby...`

### 🔴 Sleep Mode

* Eyes are **fully closed**.
* No animations, only minimal energy usage.
* Wakes automatically when audio or activity is detected.

This makes the device more engaging, friendly for kids, and clearly indicates system state without needing a phone or laptop.

![alt text](https://github.com/Neel123priyansh/Class_Owl/blob/main/img/IMG-20250405-WA0015.jpg/?raw=true)
---

### ✨ Made for classrooms, students & equitable education.

🦉 *Learn. Understand. Remember.*
