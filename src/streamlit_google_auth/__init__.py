# Thanks mkhorasani for his authentification package that I used to build this 
# https://github.com/mkhorasani/Streamlit-Authenticator

import os
import time
import streamlit as st
from typing import Literal
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

from .cookie import CookieHandler

class Authenticate:
    def __init__(self, secret_credentials_path:str, redirect_uri: str, cookie_name: str, cookie_key: str, cookie_expiry_days: float=30.0):
        st.session_state['connected']   =   st.session_state.get('connected', False) 
        self.secret_credentials_path    =   secret_credentials_path
        self.redirect_uri               =   redirect_uri
        self.cookie_handler             =   CookieHandler(cookie_name,
                                                          cookie_key,
                                                          cookie_expiry_days)
        
    def get_authorization_url(self) -> str:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.secret_credentials_path, # replace with you json credentials from your google auth app
            scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
            redirect_uri=self.redirect_uri,
        )

        authorization_url, state = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
            )
        return authorization_url

    def login(self, color:Literal['white', 'blue']='blue', justify_content: str="center") -> tuple:
        if not st.session_state['connected']:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                self.secret_credentials_path, # replace with you json credentials from your google auth app
                scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
                redirect_uri=self.redirect_uri,
            )

            authorization_url, state = flow.authorization_url(
                    access_type="offline",
                    include_granted_scopes="true",
                )
            
            html_content = f"""
<div style="display: flex; justify-content: {justify_content};">
    <a href="{authorization_url}" target="_self" style="background-color: {'#fff' if color == 'white' else '#4285f4'}; color: {'#000' if color == 'white' else '#fff'}; text-decoration: none; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; padding: 8px 12px; border-radius: 4px; display: flex; align-items: center;">
        <img src="https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA" alt="Google logo" style="margin-right: 8px; width: 26px; height: 26px; background-color: white; border: 2px solid white; border-radius: 4px;">
        Sign in with Google
    </a>
</div>
"""

            st.markdown(html_content, unsafe_allow_html=True)

    def check_authentification(self):
        if not st.session_state['connected']:
            token = self.cookie_handler.get_cookie()
            if token:
                user_info = {
                    'name': token['name'],
                    'email': token['email'],
                    'picture': token['picture'],
                    'id': token['oauth_id']
                }
                st.query_params.clear()
                st.session_state["connected"] = True
                st.session_state["user_info"] = user_info
                st.session_state["oauth_id"] = user_info.get("id")
                return
            
            time.sleep(0.3)
            
            if not st.session_state['connected']:
                auth_code = st.query_params.get("code")
                st.query_params.clear()
                if auth_code:
                    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                        self.secret_credentials_path, # replace with you json credentials from your google auth app
                        scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
                        redirect_uri=self.redirect_uri,
                    )
                    flow.fetch_token(code=auth_code)
                    credentials = flow.credentials
                    user_info_service = build(
                        serviceName="oauth2",
                        version="v2",
                        credentials=credentials,
                    )
                    user_info = user_info_service.userinfo().get().execute()

                    st.session_state["connected"] = True
                    st.session_state["oauth_id"] = user_info.get("id")
                    st.session_state["user_info"] = user_info
                    self.cookie_handler.set_cookie(user_info.get("name"), user_info.get("email"), user_info.get("picture"), user_info.get("id"))
                    st.rerun()
    
    def logout(self):
        st.session_state['logout'] = True
        st.session_state['name'] = None
        st.session_state['username'] = None
        st.session_state['connected'] = None
        self.cookie_handler.delete_cookie()
