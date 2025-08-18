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
class VenueTest(CoreTestBase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_venue(self):
        res_dict = self.create_venue('WSTS', 'WSTS in Bld ', 'AVAILABLE')
        venue_id = res_dict['venue_id']
        venue_name = res_dict['name']

        url = shared_dict['host'] + '/venues/' + venue_id

        logger.debug('GET url= %s', url)
        result = requests.get(url, headers=shared_dict['headers'])
        logger.debug('result.text: %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        json.dumps(res_dict, indent=4)

        self.assertEqual(res_dict['name'], venue_name)

        logger.debug('PATCH url= %s', url)
        url = shared_dict['host'] + '/venues/' + venue_id
        venue_location = 'room ' + str(random.randint(101,299))
        venue_update_dict = {'location': venue_location}
        result = requests.patch(url,
            headers=shared_dict['headers'],
            data=json.dumps(venue_update_dict))
        logger.debug('result.text: %s', result.text)
        self.assertEqual(result.status_code, 204)

        logger.debug('GET url= %s', url)
        result = requests.get(url, headers=shared_dict['headers'])
        logger.debug('result.text: %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)

        self.assertEqual(res_dict['location'], venue_location)

        # venue status
        url = '{0}/venues/{1}/status'.format(shared_dict['host'], venue_id)

        logger.debug('GET url= %s', url)
        result = requests.get(url, headers=shared_dict['headers'])
        logger.debug('result.text: %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['status'], 'AVAILABLE')

        test_conductor = 'skywalker'
        new_status = {'test_conductor': test_conductor, 'status': 'IN_USE'}
        logger.debug('PATCH url= %s', url)
        result = requests.patch(url,
            data=json.dumps(new_status),
            headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 204)

        logger.debug('GET url= %s', url)
        result = requests.get(url, headers=shared_dict['headers'])
        logger.debug('result.text: %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['status'], 'IN_USE')
        self.assertEqual(res_dict['test_conductor'], test_conductor)

    def test_get_venue(self):
        print('===test_get_venue:===')

        res_dict = self.create_venue('WSTS', 'WSTS in Bld ', 'AVAILABLE')

        venue_id = res_dict['venue_id']

        url = shared_dict['host'] + '/venues/' + venue_id

        print('url:', url)
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        venue_dict = json.loads(result.text)

        self.assertEqual(venue_dict['venue_id'], venue_id)
        self.assertTrue(len(venue_dict['venue_group_id']) > 0)
        self.assertEqual(venue_dict['venue_group_name'], 'Default')

        # try to get a non-existent venue
        url = url + 'non-existing'
        print('url:', url)
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 404)
        res_dict = json.loads(result.text)
        self.assertTrue(res_dict['message'].startswith(
            'No venue was found'))


    def test_get_venues(self):
        venue1 = self.create_venue('WSTS', 'WSTS in Bld ', 'AVAILABLE')
        venue2 = self.create_venue('WSTS', 'WSTS in Bld ', 'AVAILABLE')
        venue3 = self.create_venue('WSTS', 'WSTS in Bld ', 'IN_USE')
        venue4 = self.create_venue('Testbed', 'WSTS in Room ', 'IN_USE')

        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000}
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        venue_count = len(res_dict)
        self.assertGreater(len(res_dict), 3)

        # get only available venues
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'status': 'AVAILABLE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertGreater(len(res_dict), 0)
        for venue in res_dict:
            logger.debug('venue: %s', json.dumps(venue, indent=4))
            self.assertEqual(venue['venue_status']['status'], 'AVAILABLE')

        #filter venue type
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_type': 'Testbed'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertGreater(len(res_dict), 0)

        #filter venue name
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_name': 'aaaaaaaaaaaa'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 0)    

        #filter venue name
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_name': venue2['name']}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)

        #filter venue name
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_name': venue2['name'].upper()}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)    

        #filter venue name
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_name': venue2['name'][0:len(venue2['name'])-1]}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)   

        #filter venue name
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_name': venue2['name'][1:len(venue2['name'])-1]}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)   
        self.assertEqual(res_dict[0]['venue_id'], venue2['venue_id'])  

        # filter by description
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'description': 'Room'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertGreater(len(res_dict), 0)
        for venue in res_dict:
            self.assertTrue(venue['description'].find('Room') > -1)

        #filter venue group name
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_group_name': 'Default'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertGreater(len(res_dict), 0)
        for venue in res_dict:
            self.assertEqual(venue['venue_group_name'], 'Default')

        # Get all
        url = shared_dict['host'] + '/venues'
        params = {'offset': 0, 'limit': 10000}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        all_venues = json.loads(result.text)
        total_count = len(all_venues)
        
        # Apply venue status filter
        url = shared_dict['host'] + '/venues'
        params = {'status': 'IN_USE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertGreater(len(res_dict), 0)
        for venue in res_dict:
            self.assertEqual(venue['venue_status']['status'], 'IN_USE')
            
        # Apply venue status exclusion filter
        url = shared_dict['host'] + '/venues'
        params = {'exclude_status': 'IN_USE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertGreater(len(res_dict), 0)
        for venue in res_dict:
            self.assertNotEqual(venue['venue_status']['status'], 'IN_USE')              

        # Apply limit
        url = shared_dict['host'] + '/venues'
        params = {'limit': 2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), total_count)
        self.assertListEqual(res_dict, all_venues[0:2])

        # Apply offset and limit
        url = shared_dict['host'] + '/venues'
        params = {'offset': 1, 'limit': 2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), total_count)
        self.assertListEqual(res_dict, all_venues[1:3])

        # filter by description
        url = shared_dict['host'] + '/venues'
        params = {'description': 'in Bld', 'limit': 10000}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        venues_in_bld = json.loads(result.text)
        num_venues_in_bld = len(venues_in_bld)

        # filter by description and apply offset and limit
        url = shared_dict['host'] + '/venues'
        params = {'description': 'in Bld', 'offset': 1, 'limit': 2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), num_venues_in_bld)
        self.assertListEqual(res_dict, venues_in_bld[1:3])

        # filter venue group name
        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_group_name': 'Default'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertGreater(len(res_dict), 0)
        for venue in res_dict:
            self.assertEqual(venue['venue_group_name'], 'Default')

        venue_group_id = res_dict[0]['venue_group_id']

        # filter venue group status        
        url = shared_dict['host'] + '/venue_groups/' + venue_group_id
        params = {'limit': 10000, 'venue_group_name': 'Default'}
        result = requests.patch(url, json={'status': 'INACTIVE'}, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 204)

        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_group_name': 'Default', 'venue_group_status': 'ACTIVE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 0)

        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_group_name': 'Default', 'venue_group_status': 'INACTIVE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertGreater(len(res_dict), 0)
        for venue in res_dict:
            self.assertEqual(venue['venue_group_name'], 'Default')

        url = shared_dict['host'] + '/venue_groups/' + venue_group_id
        params = {'limit': 10000, 'venue_group_name': 'Default'}
        result = requests.patch(url, json={'status': 'ACTIVE'}, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 204)

        url = shared_dict['host'] + '/venues'
        params = {'limit': 10000, 'venue_group_name': 'Default', 'venue_group_status': 'ACTIVE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('venues: %s', json.dumps(res_dict, indent=4))
        self.assertGreater(len(res_dict), 0)
        for venue in res_dict:
            self.assertEqual(venue['venue_group_name'], 'Default')

    def test_delete_venue(self):
        res_dict = self.create_venue('WSTS', 'WSTS in Bld ', 'AVAILABLE')
        venue_id = res_dict['venue_id']

        url = shared_dict['host'] + '/venues/' + venue_id

        logger.debug('DELETE url= %s', url)
        result = requests.delete(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 204)

    def test_create_venue_error(self):
        url = shared_dict['host'] + '/venues'

        idx_str = random_string(10)
        # venue_name = 'wsts-' + idx_str
        # no venue name
        venue_dict = {'description': 'WSTS machine in Bld ' + idx_str}

        logger.debug('POST url= %s', url)
        result = requests.post(url,
            headers=shared_dict['headers'],
            data=json.dumps(venue_dict))

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)

        self.assertEqual(result.status_code, 400)
        self.assertTrue(result.text.find('Name was not specified') > -1)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./test-reports/"))
