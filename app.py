import streamlit as st
from datetime import date
import json
import os

st.set_page_config(layout="wide")

# =========================
# UI STYLE (BLACK BACKGROUND)
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# FILE STORAGE
# =========================
FILE_NAME = "events.json"

# =========================
# SAFE LOAD (FIXES JSON ERROR): Load your saved events from events.json and return them as a Python dictionary.
# =========================
def load_events():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            return {}
    return {}

# =========================
# SAVE EVENTS
# =========================
def save_events(events_dict):
    with open(FILE_NAME, "w") as f:
        json.dump(events_dict, f)

# =========================
# INIT SESSION STATE
# =========================
if "events" not in st.session_state:
    st.session_state.events = load_events()

# =========================
# DATE INPUT
# =========================
selected_date = st.date_input("Select a day")

today = date.today()
delta = (selected_date - today).days

# =========================
# RELATIVE DATE DISPLAY
# =========================
if delta == 0:
    st.write("Today")
elif delta == 1:
    st.write("Tomorrow")
elif delta == -1:
    st.write("Yesterday")
elif delta > 1:
    st.write(f"In {delta} days")
else:
    st.write(f"{abs(delta)} days ago")

# =========================
# EVENT INPUT
# =========================
event_text = st.text_input("Event name")
repeat = st.checkbox("Repeat every year? 🔁")

# =========================
# SAVE EVENT
# =========================
if st.button("Save Event"):
    if event_text:
        if repeat:
            key = selected_date.strftime("%m-%d")  # repeating event
        else:
            key = str(selected_date)  # one-time event

        st.session_state.events.setdefault(key, []).append({
            "text": event_text,
            "repeat": repeat
        })

        save_events(st.session_state.events)
        st.success("Event saved!")

# =========================
# DISPLAY EVENTS
# =========================
full_key = str(selected_date)
repeat_key = selected_date.strftime("%m-%d")

st.write("### Events:")

def show_event(event):
    # supports old + new formats
    if isinstance(event, dict):
        text = event["text"]
        repeat_flag = event.get("repeat", False)
    else:
        text = event
        repeat_flag = False

    if repeat_flag:
        st.write("•", text, "🔁")
    else:
        st.write("•", text)

# one-time events
if full_key in st.session_state.events:
    for event in st.session_state.events[full_key]:
        show_event(event)

# repeating events
if repeat_key in st.session_state.events:
    for event in st.session_state.events[repeat_key]:
        show_event(event)