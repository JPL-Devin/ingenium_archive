import xmlrunner
import os
import jwt
import time
import sys
import unittest
import requests
import json
import random
from config import shared_dict, logger
from ingenium_client import CoreTestBase

username = os.environ.get("USER")

def generate_token(scopes=['execute:wsts', 'execute:testbed', 'execute:sit', 'admin']):
    iat = int(time.time()) - 60
    exp = iat + (30*60)
    headers = {'Content-Type': 'application/json',
              'Accept': 'application/json'}
    private_pem = os.environ.get('PRIVATE_PEM')
    encoded_token = jwt.encode({'scopes': scopes,
                        'exp':exp,
                        'iat':iat,
                        'username': username},
                         private_pem,
                         algorithm='RS256')
   
    token_str = encoded_token.decode('utf-8')
    auth_header = 'Bearer {0}'.format(token_str)
    headers['Authorization'] = auth_header
    return headers    

class ApiKeyTest(CoreTestBase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_api_key(self):
        url = shared_dict['host'] + '/procedures'

        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)

        result = requests.get(url, headers=generate_token([]))
        # logger.info('result.text: %s', result.text)
        self.assertEqual(result.status_code, 403)

        result = requests.get(url)
        self.assertEqual(result.status_code, 401)     

        url = shared_dict['host'] + '/health'
        result = requests.get(url)
        self.assertEqual(result.status_code, 200)           


if __name__ == '__main__':
    # unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./test-reports/"))
    unittest.main()
