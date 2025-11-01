import streamlit as st



st.set_page_config(page_title="AI Classwork Chatbot", page_icon="🤖")

st.title("AI Classwork Chatbot")
st.write("Welcome! Please log in to continue.")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

role = st.radio("Select your role:", ["Student", "Professor"])


if st.button("Login"):
    if username and password:
        st.success(f"Welcome, {username}!")

        if role == "Professor":
            st.subheader("Professor Upload Page")
            uploaded_files = st.file_uploader(
                "Upload your lecture slides or assignments (PDF, PPTX, DOCX)",
                type=["pdf", "pptx", "docx"],
                accept_multiple_files=True
            )
            if uploaded_files:
                for file in uploaded_files:
                    st.success(f"Uploaded: {file.name}")
                st.info("Your files have been submitted successfully!")
            else:
                st.warning("No files uploaded yet.")
        else:
            st.subheader("Student Chatbot Page")
            st.write("Ask the AI chatbot for practice questions below.")
            user_question = st.text_input("Type your question:")
            if st.button("Ask"):
                st.write(f"Bot: Great question about '{user_question}'! More to come.")
    else:
        st.error("Please enter both username and password.")
