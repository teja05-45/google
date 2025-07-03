import streamlit as st
import requests

st.title("🗓️ AI Appointment Booking Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state.chat.append(("You", user_input))
    with st.spinner("Assistant typing..."):
        res = requests.post("http://localhost:8000/chat", json={"message": user_input})
        assistant_reply = res.json()['response']
        st.session_state.chat.append(("Assistant", assistant_reply))

for speaker, msg in st.session_state.chat:
    st.markdown(f"**{speaker}:** {msg}")