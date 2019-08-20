#!/usr/bin/python

## Uses Python 2 only

import httplib2
import requests
import logging
import pandas as pd
import time
from tqdm import tqdm
import warnings

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
logging.getLogger('oauth2client._helpers').setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

# Copy your credentials from the console
CLIENT_ID = '04214524597-e6n8keojb87fl3ap73vaprc0ic5kgv89.apps.googleusercontent.com'
CLIENT_SECRET = 'vOBcyy3xsbze3SU_mvSUS_nK'

# Check https://developers.google.com/webmaster-tools/search-console-api-original/v3/ for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Create a credential storage object.  You pick the filename.
storage = Storage('gsc_credentials')

# Attempt to load existing credentials.  Null is returned if it fails.
credentials = storage.get()

# Only attempt to get new credentials if the load failed.
if not credentials:

    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    storage.put(credentials)
    if storage.get():
        print('Credentials saved for later.')

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

webmasters_service = build('webmasters', 'v3', http=http)