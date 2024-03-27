# streamlit-google-auth

`streamlit-google-auth` is a simple package to add google authentification in your streamlit app.  
For that I use the google API, so you will need a google cloud account and to create credentials.  

## 1. Get your google credentials json

1. Go to google cloud
2. Create an account and a project
3. Go to APIs & services
4. On the left sidebar, go to Credentials
5. Anable the API
6. On the top bar, click on + CREATE CREDENTIALS and select OAuth client ID
7. Select Web application and name the it as you want
8. Add the URLs of your apps in both origins and redirect
9. You should see a new row in OAuth 2.0 Client IDs where you can download the json

## 2. Install the package

`pip install streamlit-google-auth`

## 3. login and logout

The `login` function will first check the cookies if the user already exist.  
And create a button that the user can use.

In the other hand, `logout` is just a function and a button need to be created

```python
from streamlit-google-auth import login, logout

secret_credentials_path = 'google_credentials.json'
cookie_name = 'my_cookie_name'
cookie_key = 'this_is_secret'
cookie_expiry_days = 30
app_url = 'localhost:8501'
color = 'blue' # Or 'white'
justify_content = 'center'

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
    st.write(st.session_state['user_info'].get('name'))

    if st.button('Log out'):
        logout()
```

Once the login function run, session_state will have 3 new keys ,  and ``.
- `connected` : A Boolean True if connected, False if not
- `oauth_id` : Is a unique identifier from Google
- `user_info` : Is user infos provided by google:
    - `name`
    - `email`
    - `avatar`
    - Note: you can request more when creating the google credentials json. The user will se what you are asking in the google login page.

## 4. check_cookies and get_authorization_url

If you want to implement the login in another way, you can use the `check_cookies` and `get_authorization_url` functions.  
At the start of you app, you can call `check_cookies` and if the cookie exist, the user is automatically log.  
`check_cookies` also add the keys connected, oauth_id and user_info to session_state.

```python
from streamlit-google-auth import check_cookies

check_cookies(cookie_name, cookie_key)
```

And if you just want the url that the user need to use to access the login google url.  
This is usefull if you want to do a custom button, ect.

```python
from streamlit-google-auth import get_authorization_url

get_authorization_url(secret_credentials_path, app_url)
```

Note: You can check for cookies before calling `login`
