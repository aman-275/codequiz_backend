from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
import os
from dotenv import load_dotenv
load_dotenv() 

class GoogleLogin(
    SocialLoginView
):  # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = str(os.getenv('callback_url')) # update this to config file
    client_class = OAuth2Client
