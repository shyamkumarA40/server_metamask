import streamlit as st
import json
import os
import time
import base64

USERNAME = "admin"
PASSWORD = "admin"
WALLET_SESSION_FILE = "wallet_session.json"
METAMASK_URL = "http://localhost:5000/wallet-login"  # This could be any real wallet login page

st.set_page_config(page_title="AIverse - Login")

def get_wallet_session():
    if os.path.exists(WALLET_SESSION_FILE):
        with open(WALLET_SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("wallet")
    return None

def disconnect_wallet():
    if os.path.exists(WALLET_SESSION_FILE):
        os.remove(WALLET_SESSION_FILE)
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("Disconnected successfully.")
    st.rerun()

def wallet_login():
    st.markdown("## 🦊 Login with MetaMask")

    if st.button("Login with MetaMask"):
        js = f"""
        <script>
        window.open("{METAMASK_URL}", "_blank");
        </script>
        """
        st.markdown(js, unsafe_allow_html=True)
        st.info("Opened MetaMask login in new tab. Waiting for connection...")

        with st.spinner("Waiting for wallet connection..."):
            for _ in range(30):
                wallet_address = get_wallet_session()
                if wallet_address:
                    st.session_state.authenticated = True
                    st.session_state.wallet = wallet_address
                    st.rerun()
                time.sleep(1)

        st.warning("Wallet not connected. Please try again.")

def add_login_background(image_file):
    with open(image_file, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode()

    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def login_form():
    add_login_background("images/background40.jpg")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧑 Username Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == USERNAME and password == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        wallet_login()

    if st.button("Back to Home"):
        st.session_state.show_login_form = False
        st.rerun()

def show_authenticated_content():
    st.title("🎉 Welcome to AIverse, Explorer!")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    show_authenticated_content()
else:
    login_form()

