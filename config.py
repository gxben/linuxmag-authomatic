# config.py

from authomatic.providers import oauth2, oauth1, openid

SECRET = "UUID_ALEATOIRE"

CONFIG = {

    'tw': { # Your internal provider name
        'short_name': 1,
        'class_': oauth1.Twitter,
        'consumer_key': 'MA_CLE_TWITTER',
        'consumer_secret': 'MON_SECRET_TWITTER',
    },

    'fb': {
        'class_': oauth2.Facebook,
        'short_name': 2,
        'consumer_key': 'MA_CLE_FACEBOOK',
        'consumer_secret': 'MON_SECRET_FACEBOOK',
        'scope': ['user_about_me', 'email', 'publish_stream'],
    },

    'google': {
         'class_': oauth2.Google,
         'short_name': 3,
         'consumer_key': 'MA_CLE_GOOGLE.apps.googleusercontent.com',
         'consumer_secret': 'MON_SECRET_GOOGLE',
         'scope': ['profile', 'https://www.googleapis.com/auth/plus.login', 'email']
    },
}
