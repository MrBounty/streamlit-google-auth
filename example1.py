import streamlit as st
from streamlit_google_auth import Authenticate

st.title('Streamlit Google Auth Example 1')

authenticator = Authenticate(
    secret_credentials_path = 'google_credentials.json',
    cookie_name='my_cookie_name',
    cookie_key='this_is_secret',
    redirect_uri = 'http://localhost:8501',
)

# Catch the login event
authenticator.check_authentification()

# Create the login button
authenticator.login()

if st.session_state['connected']:
    st.image(st.session_state['user_info'].get('picture'))
    st.write('Hello, '+ st.session_state['user_info'].get('name'))
    st.write('Your email is '+ st.session_state['user_info'].get('email'))
    if st.button('Log out'):
        authenticator.logout()