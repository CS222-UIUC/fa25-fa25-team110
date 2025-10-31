import streamlit as st
import requests
from datetime import datetime, timedelta

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Login", layout="centered")

def save_tokens(access, refresh):
    st.session_state["auth"] = {
        "access": access,
        "refresh": refresh,
        "access_exp": datetime.utcnow() + timedelta(minutes=14),
    }

def logged_in(): 
    return "auth" in st.session_state

def auth_headers(): 
    return {"Authorization": f"Bearer {st.session_state['auth']['access']}"}


def parse_tokens_from_url():
    qp = st.query_params
    access = qp.get("access")
    refresh = qp.get("refresh")
    if access and refresh:
        save_tokens(access, refresh)
        # Clean the URL so tokens aren’t left in history
        st.query_params.clear()
        st.rerun()

def login_button():
    login_url = f"{API_BASE}/accounts/google/login/"
    st.link_button("Continue with Google", login_url)

st.title("Login")

# If the backend redirected here with tokens, capture once:
parse_tokens_from_url()

if not logged_in():
    login_button()

else:
    st.success("You are signed in!")

    # Call protected endpoints
    me = requests.get(f"{API_BASE}/api/me/", headers=auth_headers(), timeout=10)
    st.write("**/api/me**:", me.json() if me.ok else me.text)

    pd = requests.get(f"{API_BASE}/api/protected-data/", headers=auth_headers(), timeout=10)
    st.write("**/api/protected-data**:", pd.json() if pd.ok else pd.text)

    if st.button("Log out"):
        st.session_state.pop("auth", None)
        st.rerun()