import streamlit as st

st.set_page_config(page_title="Professor Page", page_icon="📚")

st.title("Professor Upload Page")

# Check login and role before showing content
if not st.session_state.get("logged_in") or st.session_state.get("role") != "Professor":
    st.error("Access denied. Please log in as a Professor.")
    st.stop()

st.write("Upload your course materials below.")

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

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.switch_page("app.py")
