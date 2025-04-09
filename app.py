import streamlit as st
import google.generativeai as genai
import datetime
import json
import os
import re

# ✅ Load Gemini API key safely from Streamlit secrets
api_key = st.secrets["api_key"]  # Accessing directly now

# Configure the Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# ✅ Streamlit Setup
st.set_page_config(page_title="🧠 Alzheimer's Support Chatbot BY : MANISH_RAWAT", page_icon="🧠")
st.title("🧠 Alzheimer's Support Chatbot")
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

# ✅ Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = {"reminders": []}

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

# ✅ Dummy TTS
def speak(text):
    pass  # Placeholder for local TTS

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
        st.info("You can say: 'Remind me to take aspirin at 9AM'.")

    if st.button("👨‍⚕️ Emergency Contact"):
        st.info("Call:\n- Doctor: 📞 9876543210\n- Family: 📞 9123456780")

    if st.button("🔊 Toggle Voice Output"):
        st.session_state.voice_enabled = not st.session_state.voice_enabled
        st.success(f"Voice {'enabled' if st.session_state.voice_enabled else 'disabled'}")

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

# ✅ Greeting
now = datetime.datetime.now().hour
greeting = "Good morning! 🌞" if 5 <= now < 12 else "Good afternoon! ☀️" if 12 <= now < 17 else "Good evening! 🌙"
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    speak(greeting)

# ✅ Text input
user_input = st.text_input("👤 You:", key="user_input")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

# ✅ Memory logic
if st.session_state.messages:
    last_msg = st.session_state.messages[-1]["content"].lower()

    if "i had" in last_msg and "lunch" in last_msg:
        st.session_state.memory["lunch_yesterday"] = last_msg

    if "what did i have for lunch yesterday" in last_msg:
        lunch = st.session_state.memory.get("lunch_yesterday")
        reply = f"You told me: {lunch}" if lunch else "I don’t remember your lunch from yesterday."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        speak(reply)

    match = re.search(r"remind me to (.+?) at (\d{1,2} ?[apAP][mM])", last_msg)
    if match:
        task = match.group(1).strip()
        time = match.group(2).upper().replace(" ", "")
        st.session_state.memory["reminders"].append({"task": task, "time": time})
        reply = f"Okay, I will remind you to {task} at {time}."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        speak(reply)

    elif "reminders" in last_msg:
        reminders = st.session_state.memory.get("reminders", [])
        reply = "Here are your reminders:\n" + "\n".join([f"🔔 {r['task']} at {r['time']}" for r in reminders]) if reminders else "You don't have any reminders."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        speak(reply)

# ✅ Gemini response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    try:
        convo = model.start_chat(history=[
            {"role": msg["role"], "parts": [msg["content"]]}
            for msg in st.session_state.messages if msg["role"] in ["user", "assistant"]
        ])
        response = convo.send_message(st.session_state.messages[-1]["content"])
        bot_reply = response.text
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        speak(bot_reply)
    except Exception as e:
        st.error(f"❌ Gemini API Error: {e}")

# ✅ Chat Display
st.divider()
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"👤 **You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"🤖 **Bot:** {msg['content']}")
