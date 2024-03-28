import jwt
import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

def _token_decode(token, cookie_key) -> str:
    try:
        return jwt.decode(token, cookie_key, algorithms=['HS256'])
    except:
        return False
        
def _token_encode(cookie_key, cookie_expiry_days) -> str:
    return jwt.encode(
        payload = {
            'oauth_id': st.session_state['oauth_id'],
            'user_info': st.session_state['user_info'],
            'exp_date': (datetime.now() + timedelta(days=cookie_expiry_days)).timestamp()
            }, 
        key=cookie_key, 
        algorithm='HS256')

def _check_cookies(cookie_name, cookie_key):
    token = cookie_manager.get(cookie_name)
    if token is not None:
        token = _token_decode(token, cookie_key)
        if token is not False and token['exp_date'] > datetime.now().timestamp() and 'oauth_id' in token:
            st.session_state["connected"] = True
            st.session_state['oauth_id'] = token['oauth_id']
            st.session_state['user_info'] = token['user_info']
            return True
        
    st.session_state["connected"] = False
    st.session_state["oauth_id"] = None
    st.session_state["user_info"] = None
        
    return False

def set_cookies(cookie_name, cookie_key, cookie_expiry_days):
    token = _token_encode(cookie_key, cookie_expiry_days)
    cookie_manager.set(cookie_name, token,
        expires_at=datetime.now() + timedelta(days=cookie_expiry_days))
    
def _logout(cookie_name):
    st.query_params.clear()
    cookie_manager.delete(cookie_name)
    st.session_state["connected"] = False
    st.session_state["oauth_id"] = None
    st.session_state["user_info"] = None
    st.rerun()