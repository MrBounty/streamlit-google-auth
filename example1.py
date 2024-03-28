import streamlit as st
from streamlit_google_auth import login, logout

secret_credentials_path = 'google_credentials.json'
cookie_name = 'my_cookie_name'
cookie_key = 'this_is_secret'
cookie_expiry_days = 30
app_url = 'http://localhost:8501'
color = 'blue' # Or 'white'
justify_content = 'center'

st.title('Streamlit Google Auth Example 1')


login(
    secret_credentials_path=secret_credentials_path,
    cookie_name=cookie_name,
    cookie_key=cookie_key,
    cookie_expiry_days=cookie_expiry_days,
    app_url=app_url,
    color=color,
    justify_content=justify_content
)

if st.session_state['connected']:
    st.image(st.session_state['user_info'].get('picture'))
    st.write('Hello, '+ st.session_state['user_info'].get('name'))
    st.write('Your email is '+ st.session_state['user_info'].get('email'))
    if st.button('Log out'):
        logout(cookie_name)