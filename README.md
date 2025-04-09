
# 📁 Project Structure
alzheimers-chatbot/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── memory.json             # Saved user reminders
├── .streamlit/
│   └── secrets.toml        # (only for local dev, not pushed to GitHub)
└── README.md               # Project info

# 📦 Requirements
Key libraries used:

streamlit

google-generativeai

pyttsx3

speechrecognition

pyaudio (optional: only if voice input is enabled locally)

See full list in requirements.txt.

# 🧠 Alzheimer's Support Chatbot

A voice-enabled conversational chatbot designed to assist individuals with Alzheimer's by offering reminders, emotional support, and friendly conversations.

Built using **Streamlit**, powered by **Google's Gemini API**.

---

## 💡 Features

- 🗣️ Voice input & output support
- 🧘 Emotional reassurance ("I feel lost", etc.)
- 💊 Medication reminders
- 📅 Day & routine info
- 📋 Saves chat memory and reminders
- ✅ Simple UI optimized for elderly interaction

---

## 🚀 Live Demo

👉 [Try it on Streamlit Cloud](https://share.streamlit.io/your-username/alzheimers-chatbot/main/app.py)

> ⚠️ Replace the URL above after deployment.

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/alzheimers-chatbot.git
cd alzheimers-chatbot


```bash
pip install -r requirements.txt
streamlit run app.py
