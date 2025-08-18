import requests
import json
import time
import os
import jwt

from ingenium_client import shared_dict, logger

# Do not use ingenium_server which may be using the host name.
server = os.environ.get('ARCHIVE_ING_URL', 'http://127.0.0.1:8010') 
api_path = '{0}/api/v5'.format(server)
logger.debug('api_path: %s', api_path)
shared_dict['host'] = api_path


