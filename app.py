import streamlit as st
import google.generativeai as genai
import datetime
import json
import os
import re

# ✅ Deployment configuration
IS_DEPLOYED = True  # Set to False for local testing
GEMINI_API_KEY = "AIzaSyB-cEawYprfMTPOTKfzuhP8sx66-HLZ5vA"

# ✅ Conditional imports for local use only
if not IS_DEPLOYED:
    import pyttsx3
    import speech_recognition as sr

# ✅ Configure API Key
api_key = GEMINI_API_KEY if IS_DEPLOYED else st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# ✅ Streamlit Setup
st.set_page_config(page_title="🧠 Alzheimer's Support Chatbot BY MANISH_RAWAT", page_icon="🧠")
st.title("🧠 Alzheimer's Support Chatbot \n\b BY MANISH_RAWAT")
st.markdown("""
<h1>🧠 Alzheimer's Support Chatbot</h1>
<h3>By <span style='color:#FF4B4B; font-weight:bold;'>MANISH_RAWAT</span></h3>
""", unsafe_allow_html=True)

st.markdown("Welcome! This chatbot helps Alzheimer's patients with simple, friendly conversations.")
st.info("""
🧠 **How I Can Help You:**
- Ask me what day it is or who you are.
- I can remind you to take your medicine.
- I can help calm you down if you’re confused or lost.
- Just talk to me. I'm always here. ❤️
""")

# ✅ Memory Save File
MEMORY_FILE = "memory.json"

# ✅ Session states
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = {"reminders": []}

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

# ✅ TTS Function
def speak(text):
    if not IS_DEPLOYED and st.session_state.voice_enabled:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

# ✅ Voice Input Function
def get_voice_input():
    if IS_DEPLOYED:
        st.warning("🎤 Voice input is not available on Streamlit Cloud.")
        return None
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎙️ Listening... Please speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
    return None

# ✅ Sidebar
with st.sidebar:
    st.header("🧠 Options")
    if st.button("💾 Save Memory"):
        with open(MEMORY_FILE, "w") as f:
            json.dump(st.session_state.memory, f)
        st.success("Memory saved!")

    if st.button("📂 Load Memory"):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                st.session_state.memory = json.load(f)
            st.success("Memory loaded!")

    if st.button("🔁 View Reminders"):
        reminders = st.session_state.memory.get("reminders", [])
        if reminders:
            st.info("\n".join([f"🔔 {r['task']} at {r['time']}" for r in reminders]))
        else:
            st.warning("You have no reminders yet.")

    if st.button("💊 Medication Tracker"):
        st.info("You can say things like: 'Remind me to take aspirin at 9AM'.")

    if st.button("👨‍⚕️ Emergency Contact"):
        st.info("In an emergency, please call:\n- Doctor: 📞 9876543210\n- Family: 📞 9123456780")

    if st.button("🔊 Toggle Voice Output"):
        st.session_state.voice_enabled = not st.session_state.voice_enabled
        st.success(f"Voice output {'enabled' if st.session_state.voice_enabled else 'disabled'}")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages.clear()
        st.success("Chat cleared!")

    if st.button("📋 Get Summary"):
        summary = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
        st.text_area("Conversation Summary", summary, height=300)

# ✅ Quick Prompts
st.subheader("Quick Prompts")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📅 What day is it today?"):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        st.session_state.messages.append({"role": "user", "content": f"What day is it today? ({today})"})
with col2:
    if st.button("🫖 How to make tea"):
        st.session_state.messages.append({"role": "user", "content": "How do I make a cup of tea?"})
with col3:
    if st.button("🥪 What did I have for lunch yesterday?"):
        st.session_state.messages.append({"role": "user", "content": "What did I have for lunch yesterday?"})
with col4:
    if st.button("❤️ I feel lost"):
        st.session_state.messages.append({"role": "user", "content": "I feel lost. Can you help me feel better?"})

# ✅ Time-based greeting
now = datetime.datetime.now().hour
if 5 <= now < 12:
    greeting = "Good morning! 🌞"
elif 12 <= now < 17:
    greeting = "Good afternoon! ☀️"
else:
    greeting = "Good evening! 🌙"

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    speak(greeting)

# ✅ User Input (text)
user_input = st.text_input("👤 You:", key="user_input")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

# ✅ Voice Input
if not IS_DEPLOYED and st.button("🎤 Speak Instead"):
    voice_text = get_voice_input()
    if voice_text:
        st.session_state.messages.append({"role": "user", "content": voice_text})

# ✅ Memory capture logic
if st.session_state.messages:
    last_user_msg = st.session_state.messages[-1]["content"].lower()

    if "i had" in last_user_msg and "lunch" in last_user_msg:
        st.session_state.memory["lunch_yesterday"] = last_user_msg

    if "what did i have for lunch yesterday" in last_user_msg:
        lunch = st.session_state.memory.get("lunch_yesterday")
        reply = f"You told me: {lunch}" if lunch else "I'm sorry, I don't remember what you had for lunch yesterday unless you tell me."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        speak(reply)

    elif re.search(r"remind me to (.+?) at (\d{1,2} ?[apAP][mM])", last_user_msg):
        match = re.search(r"remind me to (.+?) at (\d{1,2} ?[apAP][mM])", last_user_msg)
        task = match.group(1).strip()
        time = match.group(2).upper().replace(" ", "")
        st.session_state.memory["reminders"].append({"task": task, "time": time})
        reply = f"Okay, I will remind you to {task} at {time}."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        speak(reply)

    elif "what are my reminders" in last_user_msg or "reminders" in last_user_msg:
        reminders = st.session_state.memory.get("reminders", [])
        reply = "Here are your reminders:\n" + "\n".join(
            [f"🔔 {r['task']} at {r['time']}" for r in reminders]
        ) if reminders else "You don't have any reminders saved yet."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        speak(reply)

# ✅ Use Gemini model
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    convo = model.start_chat(history=[
        {"role": msg["role"], "parts": [msg["content"]]}
        for msg in st.session_state.messages if msg["role"] in ["user", "assistant"]
    ])
    try:
        response = convo.send_message(st.session_state.messages[-1]["content"])
        bot_reply = response.text
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        speak(bot_reply)
    except Exception as e:
        st.error(f"❌ Error: {e}")

# ✅ Chat display
st.divider()
for msg in st.session_state.messages:
    role_label = "👤 **You:**" if msg["role"] == "user" else "🤖 **Bot:**"
    st.markdown(f"{role_label} {msg['content']}")
