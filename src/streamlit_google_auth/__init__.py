import streamlit as st
from typing import Literal
from ._auth import _login, _get_authorization_url, _check_authentification
from ._cookies import _logout, _check_cookies

def logout(cookie_name:str):
    """
    Logout the user by deleting the cookie and rerun the app
    
    cookie_name: str = 'my_cookie_name'
        Name of the cookie"""
    _logout(cookie_name)

def login(secret_credentials_path:str, cookie_name:str, cookie_key:str, cookie_expiry_days:int, app_url:str, color:Literal['white', 'blue']='blue', justify_content:str="center"):
    """
    Check the cookies for authentication and display the Google button to login

    secret_credentials_path: str = 'authentification/google_credentials.json'
        Path to the secret credentials file from Google API

    cookie_name: str = 'my_cookie_name'
        Name of the cookie
        
    cookie_key: str = 'my_secret_key'
        Secret key to encode the cookie
        
    cookie_expiry_days: int = 30
        Expiry date of the cookie in days
        
    app_url: str = 'http://localhost:8501'
        URL of the app to redirect to after authentication
        
    color: Literal['white', 'blue'] = 'blue'
        Color of the Google button
        
    justify_content: str = 'center'
        Justify content of the Google button"""
    _login(secret_credentials_path, cookie_name, cookie_key, cookie_expiry_days, app_url, color, justify_content)

def get_authorization_url(secret_credentials_path:str, app_url:str) -> str:
    """
    Get the authorization URL to redirect the user to Google authentication

    secret_credentials_path: str = 'authentification/google_credentials.json'
        Path to the secret credentials file from Google API

    app_url: str = 'http://localhost:8501'
        URL of the app to redirect to after authentication"""
    return _get_authorization_url(secret_credentials_path, app_url)

def check_cookies(cookie_name:str, cookie_key:str) -> bool:
    """
    Check the cookies for authentication and set the session state. 
    Return True if the user is authenticated and False otherwise.

    cookie_name: str = 'my_cookie_name'
        Name of the cookie
        
    cookie_key: str = 'my_secret_key'
        Secret key to encode the cookie"""
    return _check_cookies(cookie_name, cookie_key)

def check_authentification(secret_credentials_path:str, cookie_name:str, cookie_key:str, cookie_expiry_days:int, app_url:str):
    """
    Check the authentication of the user and set the session state

    secret_credentials_path: str = 'authentification/google_credentials.json'
        Path to the secret credentials file from Google API

    cookie_name: str = 'my_cookie_name'
        Name of the cookie
        
    cookie_key: str = 'my_secret_key'
        Secret key to encode the cookie
        
    cookie_expiry_days: int = 30
        Expiry date of the cookie in days
        
    app_url: str = 'http://localhost:8501'
        URL of the app to redirect to after authentication"""
    _check_authentification(secret_credentials_path, cookie_name, cookie_key, cookie_expiry_days, app_url)