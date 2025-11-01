import streamlit as st

st.set_page_config(page_title="Student Page", page_icon="💬")

st.title("Student Chatbot Page")

# Check login and role before showing content
if not st.session_state.get("logged_in") or st.session_state.get("role") != "Student":
    st.error("Access denied. Please log in as a Student.")
    st.stop()

st.write("Ask the AI chatbot for practice questions below!")

user_question = st.text_input("Type your question:")

if st.button("Ask"):
    if user_question:
        st.write(f"Bot: Great question about '{user_question}'! More features coming soon.")
    else:
        st.warning("Please enter a question before asking.")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.switch_page("app.py")
