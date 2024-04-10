import streamlit as st
from streamlit_google_auth import Authenticate

if 'connected' not in st.session_state:
    authenticator = Authenticate(
        secret_credentials_path = 'google_credentials.json',
        cookie_name='my_cookie_name',
        cookie_key='this_is_secret',
        redirect_uri = 'http://localhost:8501',
    )
    st.session_state["authenticator"] = authenticator

# Catch the login event
st.session_state["authenticator"].check_authentification()

st.title('Streamlit Google Auth Example 2')

if st.session_state['connected']:
    st.image(st.session_state['user_info'].get('picture'))
    st.write('Hello, '+ st.session_state['user_info'].get('name'))
    st.write('Your email is '+ st.session_state['user_info'].get('email'))
    if st.button('Log out'):
        st.session_state["authenticator"].logout()
else:
    st.write('You are not connected')
    authorization_url = st.session_state["authenticator"].get_authorization_url()
    st.markdown(f'[Login]({authorization_url})')
    st.link_button('Login', authorization_url)