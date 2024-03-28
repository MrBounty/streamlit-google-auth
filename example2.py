import streamlit as st
from streamlit_google_auth import logout, check_cookies, get_authorization_url, check_authentification

secret_credentials_path = 'google_credentials.json'
cookie_name = 'my_cookie_name'
cookie_key = 'this_is_secret'
cookie_expiry_days = 30
app_url = 'http://localhost:8501'

# Check the cookies for authentication

st.title('Streamlit Google Auth Example 2')

if not check_cookies(cookie_name, cookie_key):
    check_authentification(secret_credentials_path, cookie_name, cookie_key, cookie_expiry_days, app_url)

if st.session_state['connected']:
    st.image(st.session_state['user_info'].get('picture'))
    st.write('Hello, '+ st.session_state['user_info'].get('name'))
    st.write('Your email is '+ st.session_state['user_info'].get('email'))
    if st.button('Log out'):
        logout(cookie_name)
else:
    st.write('You are not connected')
    authorization_url = get_authorization_url(secret_credentials_path, app_url)
    st.markdown(f'[Login]({authorization_url})')
    st.link_button('Login', authorization_url)