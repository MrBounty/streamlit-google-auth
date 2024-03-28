import streamlit as st
from ._cookies import set_cookies, _check_cookies
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

def _get_authorization_url(secret_credentials_path, app_url):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        secret_credentials_path, # replace with you json credentials from your google auth app
        scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
        redirect_uri=app_url,
    )

    authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
        )
    return authorization_url

def _login(secret_credentials_path, cookie_name, cookie_key, cookie_expiry_days, app_url, color, justify_content):
    if _check_cookies(cookie_name, cookie_key):
        return
    
    _check_authentification(secret_credentials_path, cookie_name, cookie_key, cookie_expiry_days, app_url)
    
    authorization_url = _get_authorization_url(secret_credentials_path, app_url)
    
    html_content = """
<div style="display: flex; justify-content: p_justify_content;">
<a href="p_authorization_url" target="_self" style="background-color: p_color_background; color: p_color_text; text-decoration: none; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; padding: 8px 12px; border-radius: 4px; display: flex; align-items: center;">
    <img src="https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA" alt="Google logo" style="margin-right: 8px; width: 26px; height: 26px; background-color: white; border: 2px solid white; border-radius: 4px;">
    Sign in with Google
</a>
</div>"""
    html_content = html_content.replace("p_justify_content", justify_content)
    html_content = html_content.replace("p_authorization_url", authorization_url)
    if color == 'white':
        html_content = html_content.replace("p_color_background", "#ffffff")
        html_content = html_content.replace("p_color_text", "#000000")
    else:
        html_content = html_content.replace("p_color_background", "#4285F4")
        html_content = html_content.replace("p_color_text", "#ffffff")

    st.markdown(html_content, unsafe_allow_html=True)

def _check_authentification(secret_credentials_path, cookie_name, cookie_key, cookie_expiry_days, app_url):
    auth_code = st.query_params.get("code")
    st.query_params.clear()
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            secret_credentials_path, # replace with you json credentials from your google auth app
            scopes=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
            redirect_uri=app_url,
            )
    if auth_code:
        try:
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            user_info_service = build(
                serviceName="oauth2",
                version="v2",
                credentials=credentials,
            )
            user_info = user_info_service.userinfo().get().execute()

            st.session_state["connected"] = True
            st.session_state["oauth_id"] = auth_code
            st.session_state["user_info"] = user_info
                
            set_cookies(cookie_name, cookie_key, cookie_expiry_days)

        except Exception as e:
            st.error("Authentication failed: %s" % e)
            st.session_state["connected"] = False
            st.session_state["oauth_id"] = None
            st.session_state["user_info"] = None

    st.session_state["connected"] = False
    st.session_state["oauth_id"] = None
    st.session_state["user_info"] = None