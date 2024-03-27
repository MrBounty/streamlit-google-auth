import streamlit as st
from _auth import _login
from _cookies import _logout
from typing import Literal

def login(secret_credentials_path:str, cookie_name:str, cookie_key:str, cookie_expiry_days:int, app_url:str, color:Literal['white', 'blue']='blue', justify_content:str="center"):
    """
    secret_credentials_path: str = 'authentification/google_credentials.json'
        Path to the secret credentials file from Google API

    cookie_name: str = 'my_cookie_name'
        Name of the cookie
        
    cookie_key: str = 'my_secret_key'
        Secret key to encode the cookie
        
    cookie_expiry_days: int = 30
        Expiry date of the cookie in days
        
    app_url: str = 'localhost:8501'
        URL of the app to redirect to after authentication
        
    color: Literal['white', 'blue'] = 'blue'
        Color of the Google button
        
    justify_content: str = 'center'
        Justify content of the Google button"""
    st.session_state["connected"] = False
    st.session_state["oauth_id"] = None
    st.session_state["user_info"] = None
    st.session_state['cookie_name'] = cookie_name
    _login(secret_credentials_path, cookie_name, cookie_key, cookie_expiry_days, app_url, color, justify_content)

def logout():
    _logout(st.session_state['cookie_name'])