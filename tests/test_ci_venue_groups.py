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

# ingenium_client.main.error_handling = ErrorHandling.THROW
class VenueGroupTest(CoreTestBase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_venue_group(self, name, description, status):
        url = shared_dict['host'] + '/venue_groups'

        logger.debug('GET url= %s', url)
        venue_group_input = {
            'name': name,
            'description': description,
            'status': status
        }
        result = requests.post(url, json=venue_group_input, headers=shared_dict['headers'])
        logger.debug('result.text: %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        json.dumps(res_dict, indent=4)

        return res_dict

    def test_create_venue_group(self):
        idx_str = random_string(10)
        group_name = 'group name ' + idx_str
        group_description = 'group description ' + idx_str
        status = 'ACTIVE'
        res_dict = self.create_venue_group(group_name, group_description, status)
        venue_group_id = res_dict['venue_group_id']
        venue_group_name = res_dict['name']

        self.assertEqual(venue_group_name, group_name)

        url = shared_dict['host'] + '/venue_groups/' + venue_group_id

        logger.debug('GET url= %s', url)
        result = requests.get(url, headers=shared_dict['headers'])
        logger.debug('result.text: %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        json.dumps(res_dict, indent=4)

        self.assertEqual(res_dict['name'], venue_group_name)

        logger.debug('PATCH url= %s', url)
        url = shared_dict['host'] + '/venue_groups/' + venue_group_id
        venue_group_new_name = 'group new name ' + idx_str
        venue_group_update_dict = {'name': venue_group_new_name, 'status': 'INACTIVE'}
        result = requests.patch(url,
            headers=shared_dict['headers'],
            json=venue_group_update_dict)
        logger.debug('result.text: %s', result.text)
        self.assertEqual(result.status_code, 204)

        logger.debug('GET url= %s', url)
        result = requests.get(url, headers=shared_dict['headers'])
        logger.debug('result.text: %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)

        self.assertEqual(res_dict['name'], venue_group_update_dict['name'])
        self.assertEqual(res_dict['status'], venue_group_update_dict['status'])

    def test_get_venue_group(self):
        idx_str = random_string(10)
        group_name = 'group name ' + idx_str
        group_description = 'group description ' + idx_str
        status = 'ACTIVE'
        res_dict = self.create_venue_group(group_name, group_description, status)
        venue_group_id = res_dict['venue_group_id']
        venue_group_name = res_dict['name']

        url = shared_dict['host'] + '/venue_groups/' + venue_group_id

        print('url:', url)
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        venue_group_dict = json.loads(result.text)

        self.assertEqual(venue_group_dict['venue_group_id'], venue_group_id)
        self.assertEqual(venue_group_dict['name'], group_name)
        self.assertEqual(venue_group_dict['description'], group_description)

        # try to get a non-existent venue group
        url = url + 'non-existing'
        print('url:', url)
        result = requests.get(url, headers=shared_dict['headers'])
        print('result.text:', result.text)
        self.assertEqual(result.status_code, 404)
        res_dict = json.loads(result.text)
        self.assertTrue(res_dict['message'].startswith(
            'No venue group was found'))


    def test_get_venue_groups(self):
        idx_str = random_string(10)
        group_name_1 = 'group name ' + idx_str
        group_description_1 = 'group description ' + idx_str
        status_1 = 'ACTIVE'
        res_dict_1 = self.create_venue_group(group_name_1, group_description_1, status_1)

        idx_str = random_string(10)
        group_name_2 = 'group name ' + idx_str
        group_description_2 = 'group description ' + idx_str
        status_2 = 'ACTIVE'
        res_dict_2 = self.create_venue_group(group_name_2, group_description_2, status_2)

        idx_str = random_string(10)
        group_name_3 = 'group name ' + idx_str
        group_description_3 = 'group description ' + idx_str
        status_3 = 'INACTIVE'
        res_dict_3 = self.create_venue_group(group_name_3, group_description_3, status_3)

        idx_str = random_string(10)
        group_name_4 = 'group name ' + idx_str
        group_description_4 = 'my description ' + idx_str
        status_4 = 'ACTIVE'
        res_dict_4 = self.create_venue_group(group_name_4, group_description_4, status_4)

        url = shared_dict['host'] + '/venue_groups'
        params = {'limit': 10000}
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venue_groups: %s', json.dumps(res_dict, indent=4))
        venue_group_count = len(res_dict)
        self.assertGreater(len(res_dict), 3)

        # get only active venue groups
        url = shared_dict['host'] + '/venue_groups'
        params = {'limit': 10000, 'status': 'ACTIVE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venue_groups: %s', json.dumps(res_dict, indent=4))
        self.assertGreater(len(res_dict), 0)
        for venue_group in res_dict:
            logger.debug('venue_group: %s', json.dumps(venue_group, indent=4))
            self.assertEqual(venue_group['status'], 'ACTIVE')

        # filter venue group name
        url = shared_dict['host'] + '/venue_groups'
        params = {'limit': 10000, 'venue_group_name': 'aaaaaaaaaaaa'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venue_groups: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 0)    

        # filter venue group name
        url = shared_dict['host'] + '/venue_groups'
        params = {'limit': 10000, 'venue_group_name': group_name_2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venue_groups: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)

        # filter venue group name
        url = shared_dict['host'] + '/venue_groups'
        params = {'limit': 10000, 'venue_group_name': group_name_2.upper()}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venue_groups: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)    

        # filter venue group name
        url = shared_dict['host'] + '/venue_groups'
        params = {'limit': 10000, 'venue_group_name': group_name_2[0:len(group_name_2)-1]}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venue_groups: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)   

        #filter venue group name
        url = shared_dict['host'] + '/venue_groups'
        params = {'limit': 10000, 'venue_group_name': group_name_2[1:len(group_name_2)-1]}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venue_groups: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)   
        self.assertEqual(res_dict[0]['venue_group_id'], res_dict_2['venue_group_id'])  

        # filter by description
        url = shared_dict['host'] + '/venue_groups'
        params = {'limit': 10000, 'description': 'my'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertGreater(len(res_dict), 0)
        for venue_group in res_dict:
            self.assertTrue(venue_group['description'].find('my') > -1)

        # Get all
        url = shared_dict['host'] + '/venue_groups'
        params = {'offset': 0, 'limit': 10000}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        all_venue_groups = json.loads(result.text)
        total_count = len(all_venue_groups)
                  
        # Apply limit
        url = shared_dict['host'] + '/venue_groups'
        params = {'limit': 2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), total_count)
        self.assertListEqual(res_dict, all_venue_groups[0:2])

        # Apply offset and limit
        url = shared_dict['host'] + '/venue_groups'
        params = {'offset': 1, 'limit': 2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), total_count)
        self.assertListEqual(res_dict, all_venue_groups[1:3])

        # filter by description
        url = shared_dict['host'] + '/venue_groups'
        params = {'description': 'group', 'limit': 10000}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        venue_groups_with_group = json.loads(result.text)
        num_venue_groups_with_group = len(venue_groups_with_group)

        # filter by description and apply offset and limit
        url = shared_dict['host'] + '/venue_groups'
        params = {'description': 'group', 'offset': 1, 'limit': 2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), num_venue_groups_with_group)
        self.assertListEqual(res_dict, venue_groups_with_group[1:3])

    @unittest.skip("no API to delete venue group. Change its status to INACTIVE instead")
    def test_delete_venue_group(self):
        idx_str = random_string(10)
        group_name = 'group name ' + idx_str
        group_description = 'group description ' + idx_str
        status = 'ACTIVE'
        res_dict = self.create_venue_group(group_name, group_description, status)
        venue_group_id = res_dict['venue_group_id']

        url = shared_dict['host'] + '/venue_groups/' + venue_group_id

        logger.debug('DELETE url= %s', url)
        result = requests.delete(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 204)

        result = requests.get(url, headers=shared_dict['headers'])
        print('result.text:', result.text)
        self.assertEqual(result.status_code, 404)
        res_dict = json.loads(result.text)
        self.assertTrue(res_dict['message'].startswith(
            'No venue group was found'))
        
    def test_update_venue_group(self):
        idx_str = random_string(10)
        group_name = 'group name ' + idx_str
        group_description = 'group description ' + idx_str
        status = 'ACTIVE'
        res_dict = self.create_venue_group(group_name, group_description, status)
        venue_group_id = res_dict['venue_group_id']

        url = shared_dict['host'] + '/venue_groups/' + venue_group_id

        logger.debug('PATCH url= %s', url)
        venue_group_input = {
            'name': 'modified name',
            'description': 'modified description',
            'status': 'INACTIVE'
        }
        result = requests.patch(url, json=venue_group_input, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 204)

        result = requests.get(url, headers=shared_dict['headers'])
        print('result.text:', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['name'], venue_group_input['name'])
        self.assertEqual(res_dict['description'], venue_group_input['description'])
        self.assertEqual(res_dict['status'], venue_group_input['status'])

    def test_create_venue_group_error(self):
        url = shared_dict['host'] + '/venue_groups'
        idx_str = random_string(10)
        venue_group_dict = {'description': 'group description ' + idx_str, 'status': 'ACTIVE'}

        logger.debug('POST url= %s', url)
        result = requests.post(url,
            headers=shared_dict['headers'],
            json=venue_group_dict)

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)

        self.assertEqual(result.status_code, 400)
        self.assertTrue(result.text.find('Name was not specified for venue group') > -1)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./test-reports/"))
