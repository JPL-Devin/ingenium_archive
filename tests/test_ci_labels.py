import xmlrunner
import os
import sys
import unittest
import requests
import json
import random
from config import shared_dict, logger
from test_utils import random_string
import ingenium_client
from ingenium_client import CoreTestBase, ErrorHandling

class LabelTest(CoreTestBase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_label(self):

        url = shared_dict['host'] + '/procedures/labels'
        procedure_label = {'name':'Europa', 'description':'Some europa label'}

        result = requests.post(url,
            headers=shared_dict['headers'],
            data=json.dumps(procedure_label))
        
        self.assertEqual(result.status_code, 200)


    def test_get_procedure_labels(self):

        url = shared_dict['host'] + '/procedures/labels'
        procedure_label = {'name':'Europa', 'description':'Some europa label'}

        result = requests.post(url,
            headers=shared_dict['headers'],
            data=json.dumps(procedure_label))
        
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertGreater(len(res_dict), 0)


    def test_delete_procedure_label(self):
        url = shared_dict['host'] + '/procedures/labels'
        procedure_label = {'name':'Europa', 'description':'Some europa label'}

        result = requests.post(url,
            headers=shared_dict['headers'],
            data=json.dumps(procedure_label))
        
        self.assertEqual(result.status_code, 200)
        
        res_dict = json.loads(result.text)
    
        label_id = res_dict['label_id']

        url = shared_dict['host'] + '/procedures/labels/' + label_id

        logger.debug('DELETE url= %s', url)
        result = requests.delete(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 204)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./test-reports/"))
