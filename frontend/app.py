import streamlit as st

# Page setup
st.set_page_config(page_title="AI Classwork Chatbot", page_icon="🤖")

st.title("AI Classwork Chatbot")
st.write("Welcome! Please log in to continue.")

# Input fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")
role = st.radio("Select your role:", ["Student", "Professor"])

# Session state setup to track login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# Login button logic
if st.button("Login"):
    if username and password:
        st.session_state.logged_in = True
        st.session_state.role = role
        st.success(f"Welcome, {username}! Redirecting to your {role} page...")

        # Auto-redirect to the correct page
        if role == "Professor":
            st.switch_page("pages/professor.py")
        else:
            st.switch_page("pages/student.py")
    else:
        st.error("Please enter both username and password.")


# # Display role-specific pages after login
# if st.session_state.logged_in:
#     if st.session_state.role == "Professor":
#         st.subheader("Professor Upload Page")
#         uploaded_files = st.file_uploader(
#             "Upload your lecture slides or assignments (PDF, PPTX, DOCX)",
#             type=["pdf", "pptx", "docx"],
#             accept_multiple_files=True
#         )
#         if uploaded_files:
#             for file in uploaded_files:
#                 st.success(f"Uploaded: {file.name}")
#             st.info("Your files have been submitted successfully!")
#         else:
#             st.warning("No files uploaded yet.")
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.role = None
#             st.rerun()

#     elif st.session_state.role == "Student":
#         st.subheader("Student Chatbot Page")
#         st.write("Ask the AI chatbot for practice questions below.")
#         user_question = st.text_input("Type your question:")
#         if st.button("Ask"):
#             st.write(f"Bot: Great question about '{user_question}'! More to come.")
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.role = None
#             st.rerun()
