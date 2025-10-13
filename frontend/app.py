import streamlit as st

st.set_page_config(page_title="AI Classwork Chatbot", page_icon="🤖")

st.title("AI Classwork Chatbot")
st.write("Welcome! Please log in to continue.")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username and password:
        st.success(f"Welcome, {username}!")
    else:
        st.error("Please enter both username and password.")
