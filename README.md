# Streamlit Google Auth
This package provides a simple and easy-to-use integration of Google authentication in your Streamlit application.

## Getting Started
1. Install the package:  
`pip install streamlit-google-auth`

2. Create a Google Cloud Platform project and obtain the client ID and client secret. You can follow the instructions [here](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred) to create the credentials.

3. Save the client ID and client secret in a JSON file (e.g., google_credentials.json).

4. Import the necessary modules and initialize the Authenticate class:  
    ```python
    import streamlit as st
    from streamlit_google_auth import Authenticate

    authenticator = Authenticate(
        secret_credentials_path='google_credentials.json',
        cookie_name='my_cookie_name',
        cookie_key='this_is_secret',
        redirect_uri='http://localhost:8501',
    )
    ```

5. Check if the user is already authenticated and handle the login/logout flow:
    ```python
    # Check if the user is already authenticated
    authenticator.check_authentification()

    # Display the login button if the user is not authenticated
    if not st.session_state.get('connected', False):
        authorization_url = authenticator.get_authorization_url()
        st.markdown(f'[Login]({authorization_url})')
        st.link_button('Login', authorization_url)
    # Display the user information and logout button if the user is authenticated
    else:
        st.image(st.session_state['user_info'].get('picture'))
        st.write(f"Hello, {st.session_state['user_info'].get('name')}")
        st.write(f"Your email is {st.session_state['user_info'].get('email')}")
        if st.button('Log out'):
            authenticator.logout()
    ```

That's it! Your Streamlit app now has Google authentication integrated.

## Configuration
The Authenticate class takes the following parameters:

- `secret_credentials_path`: The path to the Google Cloud Platform credentials JSON file.
- `cookie_name`: The name of the cookie used to store the authentication information.
- `cookie_key`: The secret key used to encrypt the cookie.
- `redirect_uri`: The redirect URI of your Streamlit application.
- `cookie_expiry_days`: Optional, The number of days the cookie stay valid.

## Functions
The Authenticate class provides the following functions:
- `check_authentification()`: Catch the event when the user come back from the google login page and log it.
- `login()`: Displays the login button and handles the authentication flow.
- `logout()`: Logs out the user and clears the session state.
- `get_authorization_url()`: Returns the URL for the Google authentication page.

## Session State
The Authenticate class updates the following keys in the Streamlit session state:
- `connected`: A boolean indicating whether the user is authenticated or not.
- `oauth_id`: The unique identifier for the authenticated user.
- `user_info`: A dictionary containing the user's name, email, and profile picture URL.

## Example
Here's a complete example of how to use the Authenticate class in a Streamlit app:

```python
import streamlit as st
from streamlit_google_auth import Authenticate

st.title('Streamlit Google Auth Example')

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

# Create the login button
st.session_state["authenticator"].login()

if st.session_state['connected']:
    st.image(st.session_state['user_info'].get('picture'))
    st.write('Hello, '+ st.session_state['user_info'].get('name'))
    st.write('Your email is '+ st.session_state['user_info'].get('email'))
    if st.button('Log out'):
        st.session_state["authenticator"].logout()
```