import xmlrunner
import os
import sys
import unittest
import requests
import json
import random
from config import shared_dict, logger
from test_utils import random_string
import time
from ingenium_client import CoreTestBase, StepTypes


class ProcedureTest(CoreTestBase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_procedure(self):
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        res_dict = self.create_procedure(title_1, 'First procedure', '', 'hongmank')

        procedure_id = res_dict['procedure_id']

        procedure_dict = self.get_procedure(procedure_id)

        self.assertEqual(procedure_dict['procedure_id'], procedure_id)
        self.assertEqual(procedure_dict['title'], title_1)

        # get working copy
        version_dict = self.get_procedure_version(procedure_id, 0)
        logger.debug('version_dict: %s', json.dumps(version_dict, indent=4))
        self.assertEqual(version_dict['time_versioned'], '')
        self.assertEqual(version_dict['time_released'], '')

        # update procedure
        title_new = 'Updated title'
        self.update_procedure(procedure_id, {'title': title_new})
        procedure_dict = self.get_procedure(procedure_id)
        self.assertEqual(procedure_dict['title'], title_new)


        # get working copy
        version_dict = self.get_procedure_version(procedure_id, 0)
        logger.debug('version_dict: %s', json.dumps(version_dict, indent=4))
        self.assertEqual(version_dict['time_versioned'], '')
        self.assertEqual(version_dict['time_released'], '')

        # delete procedure
        self.delete_procedure(procedure_id)

        # should not be found
        self.get_procedure(procedure_id, 400)

    def test_procedure_input_validation(self):
        url = shared_dict['host'] + '/procedures'

        # locked_by is not allowed
        procedure_dict = {'title': '',
                          'description': '',
                          'institutional_id': '',
                          'author': '',
                          'locked_by': ''}

        logger.debug('POST url= %s', url)
        result = requests.post(url,
            headers=shared_dict['headers'],
            json=procedure_dict)

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 400)


        # create a procedure
        rand_1 = random_string()
        title_1 = 'title_' + rand_1

        res_dict = self.create_procedure(title_1, 'First procedure', '', 'hongmank')

        procedure_id = res_dict['procedure_id']

        procedure_dict = self.get_procedure(procedure_id)

        self.assertEqual(procedure_dict['procedure_id'], procedure_id)
        self.assertEqual(procedure_dict['title'], title_1)

        # update procedure
        url = '{0}/procedures/{1}'.format(shared_dict['host'], procedure_id)

        logger.debug('PATCH url= %s', url)
        # title is allowed
        result = requests.patch(url,
            headers=shared_dict['headers'],
            json={'title': 'new title'})

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 204)

        logger.debug('PATCH url= %s', url)
        # locked_by is allowed
        result = requests.patch(url,
            headers=shared_dict['headers'],
            json={'locked_by': 'hongmank'})

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 204)

        logger.debug('PATCH url= %s', url)
        # time_saved is not allowed
        result = requests.patch(url,
            headers=shared_dict['headers'],
            json={'time_saved': ''})

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 400)

        ### input validation for version
        url = '{0}/procedures/{1}/versions'.format(shared_dict['host'], procedure_id)

        # version is not allowed
        version_dict = {'version_description': '',
                          'version_author': '',
                          'version': 0}

        logger.debug('POST url= %s', url)
        result = requests.post(url,
            headers=shared_dict['headers'],
            json=version_dict)

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 400)

        version_dict = self.create_procedure_version(procedure_id, '', '')
        version = version_dict['version']
        self.assertEqual(version, 1)

        url = '{0}/procedures/{1}/versions/{2}'.format(shared_dict['host'], procedure_id, version)

        # version_description is allowed
        result = requests.patch(url,
            headers=shared_dict['headers'],
            json={'version_description': 'new version description'})

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 200)

        # flight_dictionary_version is allowed
        result = requests.patch(url,
            headers=shared_dict['headers'],
            json={'flight_dictionary_version': 'v2'})

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 200)

        # time_saved is not allowed
        result = requests.patch(url,
            headers=shared_dict['headers'],
            json={'time_saved': ''})

        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 400)



    def test_get_procedures(self):
        # use this to find procedures created only from this test
        rand_0 = random_string()

        rand_1 = random_string()
        title_1 = 'title_{0}_{1}'.format(rand_0, rand_1)
        institutional_id_1 = 'pbat-101-' + rand_1
        procedure_dict = self.create_procedure(title_1, 'First procedure', institutional_id_1, 'hongmank')
        procedure_id_1 = procedure_dict['procedure_id']

        rand_2 = random_string()
        title_2 = 'title_{0}_{1}'.format(rand_0, rand_2)
        author_2 = 'author_' + rand_2
        institutional_id_2 = 'pbat-120-' + rand_2
        description_2 = 'Second procedure ' + rand_2
        procedure_dict = self.create_procedure(title_2, description_2, institutional_id_2, author_2)
        procedure_id_2 = procedure_dict['procedure_id']

        self.update_procedure(procedure_id_2, {'obsolete': True})

        rand_3 = random_string()
        title_3 = 'title_{0}_{1}'.format(rand_0, rand_3)
        institutional_id_3 = 'pbat-121-' + rand_3
        procedure_dict = self.create_procedure(title_3, 'Third procedure', institutional_id_3, 'hongmank')
        procedure_id_3 = procedure_dict['procedure_id']

        version_dict_3 = self.create_procedure_version(procedure_id_3, 'first version', 'hongmank')

        rand_4 = random_string()
        title_4 = 'title_{0}_{1}'.format(rand_0, rand_4)
        institutional_id_4 = 'pbat-123-' + rand_4
        procedure_dict = self.create_procedure(title_4, 'Fourth procedure', institutional_id_4, 'hongmank')
        procedure_id_4 = procedure_dict['procedure_id']

        version_dict_4 = self.create_procedure_version(procedure_id_4, 'first version', 'hongmank')
        self.update_procedure_version(procedure_id_4, 1, {'institutional_release_id': 'r1'})
        self.update_procedure_version_status(procedure_id_4, 1, {'action': 'RELEASE'})

        url = shared_dict['host'] + '/procedures'
        params = {'limit': 10000, 'title': rand_0}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('procedures: %s', json.dumps(res_dict, indent=4))
        venue_count = len(res_dict)
        self.assertEqual(len(res_dict), 4)

        # check for the default sort
        self.assertEqual(res_dict[0]['title'], title_4)

        # filter by title
        params = {'title': rand_1}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['title'], title_1)

        # filter by author
        params = {'title': rand_0, 'author': rand_2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['author'], author_2)

        # filter by description
        params = {'title': rand_0, 'description': rand_2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['description'], description_2)

        # filter by institutional_id
        params = {'title': rand_0, 'institutional_id': rand_4}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['institutional_id'], institutional_id_4)

        # filter by versioned
        params = {'title': rand_0, 'versioned': 'true'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)

        params = {'title': rand_0, 'versioned': 'false'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)

        # filter by released
        params = {'title': rand_0, 'released': 'true'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('procedures: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)

        params = {'title': rand_0, 'released': 'false'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('procedures: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 3)

        # filter by obsolete
        params = {'title': rand_0, 'obsolete': 'true'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)

        params = {'title': rand_0, 'obsolete': 'false'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 3)


        # unset institutional_release_id
        self.update_procedure_version_status(procedure_id_4, version_dict_4['version'], {'action': 'UNRELEASE'})
        # filter by released
        params = {'title': rand_0, 'released': 'true'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('procedures: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 0)

        params = {'title': rand_0, 'released': 'false'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('procedures: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 4)

        # check for the sort
        params = {'limit': 10000, 'title': rand_0, 'sort': 'DESC'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[0]['title'], title_4)

        params = {'limit': 10000, 'title': rand_0, 'sort': 'ASC'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[-1]['title'], title_4)
        self.assertEqual(res_dict[-2]['title'], title_3)
        self.assertEqual(res_dict[-3]['title'], title_2)
        self.assertEqual(res_dict[-4]['title'], title_1)

        params = {'limit': 10000, 'title': rand_0, 'sort': 'ASC', 'sort_by': 'TIME_CREATED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[-1]['title'], title_4)
        self.assertEqual(res_dict[-2]['title'], title_3)
        self.assertEqual(res_dict[-3]['title'], title_2)
        self.assertEqual(res_dict[-4]['title'], title_1)

        params = {'limit': 10000, 'title': rand_0, 'sort': 'ASC', 'sort_by': 'INSTITUTIONAL_ID'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[-1]['institutional_id'], institutional_id_4)
        self.assertEqual(res_dict[-2]['institutional_id'], institutional_id_3)
        self.assertEqual(res_dict[-3]['institutional_id'], institutional_id_2)
        self.assertEqual(res_dict[-4]['institutional_id'], institutional_id_1)

        params = {'limit': 10000, 'title': rand_0, 'sort': 'DESC', 'sort_by': 'INSTITUTIONAL_ID'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[-1]['institutional_id'], institutional_id_1)
        self.assertEqual(res_dict[-2]['institutional_id'], institutional_id_2)
        self.assertEqual(res_dict[-3]['institutional_id'], institutional_id_3)
        self.assertEqual(res_dict[-4]['institutional_id'], institutional_id_4)
        self.assertEqual(len(res_dict), 4)

        # get total count
        params = {'limit': 10000, 'title': rand_0, 'sort': 'DESC', 'sort_by': 'INSTITUTIONAL_ID'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        total_count = len(res_dict)

        # offset and limit
        params = {'limit': 2, 'title': rand_0}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), total_count)

        params = {'offset': 1, 'limit': 2, 'title': rand_0}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), 4)
        self.assertEqual(res_dict[0]['title'], title_3)
        self.assertEqual(res_dict[1]['title'], title_2)

    def test_create_procedure(self):
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']

        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section 1
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1')

        section_1 = res['elem']
        self.assertEqual(section_1['parent_id'], '')
        section_1_id = section_1['elem_id']
        # logger.debug('section_1: %s', json.dumps(section_1, indent=4))
        self.assertEqual(len(res['numbers']), 1)
        self.assertEqual(res['numbers'][0]['elem_id'], section_1_id)
        self.assertEqual(res['numbers'][0]['number'], '1')        

        self.assertEqual(len(res['elem_ids']), 1)
        self.assertEqual(res['elem_ids'][0], section_1_id)    

        new_description = 'Updated Section 1'
        self.update_section(procedure_url, section_1_id, {'description': new_description})

        section_1 = self.get_section(procedure_url, section_1_id)
        self.assertEqual(section_1['description'], new_description)

        # Add section 2
        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='SIBLING',
            description='Section 2')

        section_2 = res['elem']
        self.assertEqual(section_2['parent_id'], '')
        section_2_id = section_2['elem_id']
        self.assertEqual(len(res['numbers']), 1)
        self.assertEqual(res['numbers'][0]['elem_id'], section_2_id)
        self.assertEqual(res['numbers'][0]['number'], '2')        

        self.assertEqual(len(res['elem_ids']), 2)
        self.assertEqual(res['elem_ids'][0], section_1_id) 
        self.assertEqual(res['elem_ids'][1], section_2_id)

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='CHILD',
            description='Paragraph 1-1')

        paragraph_1_1 = res['elem']
        self.assertEqual(paragraph_1_1['parent_id'], section_1_id)
        paragraph_1_1_id = paragraph_1_1['elem_id']

        logger.debug('paragraph_1_1: %s', json.dumps(paragraph_1_1, indent=4))

        self.assertEqual(len(res['numbers']), 1)      
        self.assertEqual(res['numbers'][0]['elem_id'], paragraph_1_1_id)   
        self.assertEqual(res['numbers'][0]['number'], '1-1')      

        self.assertEqual(len(res['elem_ids']), 3)
        self.assertEqual(res['elem_ids'][0], section_1_id) 
        self.assertEqual(res['elem_ids'][1], paragraph_1_1_id)
        self.assertEqual(res['elem_ids'][2], section_2_id)        

        new_description = 'Updated Paragraph 1-1'
        self.update_paragraph(procedure_url, paragraph_1_1_id, {'description': new_description})

        paragraph_1_1 = self.get_paragraph(procedure_url, paragraph_1_1_id)
        self.assertEqual(paragraph_1_1['description'], new_description)

        # add step 1-2
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=paragraph_1_1_id,
            level='SIBLING',
            title='Step 1-2',
            description='Step 1-2')

        step_1_2 = res['elem']       
        self.assertEqual(step_1_2['parent_id'], section_1_id)
        step_1_2_id = step_1_2['elem_id']
        self.assertEqual(len(res['numbers']), 1)
        self.assertEqual(res['numbers'][0]['elem_id'], step_1_2_id)
        self.assertEqual(res['numbers'][0]['number'], '1-2')        

        self.assertEqual(len(res['elem_ids']), 4)
        self.assertEqual(res['elem_ids'][0], section_1_id) 
        self.assertEqual(res['elem_ids'][1], paragraph_1_1_id)
        self.assertEqual(res['elem_ids'][2], step_1_2_id)        
        self.assertEqual(res['elem_ids'][3], section_2_id)

        new_description = 'Updated Step 1-2'
        self.update_step_generic(procedure_url, step_1_2_id, {'description': new_description})

        step_1_2 = self.get_step_generic(procedure_url, step_1_2_id)
        self.assertEqual(step_1_2['description'], new_description)

        authoring_user_input = {
            'temperature': {
                'verify_on': 'VALUE',
                'verification_condition': 'RECORD',
                'verification_values': []
            },
            'humidity': {
                'verify_on': 'VALUE',
                'verification_condition': 'RECORD',
                'verification_values': []
            }
        }
        self.set_step_input_generic(procedure_url, step_1_2_id, authoring_user_input)

        res_dict = self.get_step_input_generic(procedure_url, step_1_2_id)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertDictEqual(res_dict, authoring_user_input)

        # add step 1-3
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=step_1_2_id,
            level='SIBLING',
            title='',
            description='Step 1-3')   

        step_1_3 = res['elem']
        self.assertEqual(step_1_3['parent_id'], section_1_id)
        step_1_3_id = step_1_3['elem_id']

        self.assertEqual(len(res['numbers']), 1)
        self.assertEqual(res['numbers'][0]['elem_id'], step_1_3_id)
        self.assertEqual(res['numbers'][0]['number'], '1-3')        

        self.assertEqual(len(res['elem_ids']), 5)
        self.assertEqual(res['elem_ids'][0], section_1_id) 
        self.assertEqual(res['elem_ids'][1], paragraph_1_1_id)
        self.assertEqual(res['elem_ids'][2], step_1_2_id)        
        self.assertEqual(res['elem_ids'][3], step_1_3_id) 
        self.assertEqual(res['elem_ids'][4], section_2_id)  

        res = self.update_element(procedure_url, step_1_3_id, {'title': 'Step 1-3'}) 
        logger.debug(json.dumps(res, indent=4))
        self.assertEqual(res['title'], 'Step 1-3')     
        self.assertEqual(res['description'], 'Step 1-3')     

        # get elements
        elems = self.get_elements(procedure_url)
        logger.debug('elems: %s', json.dumps(elems, indent=4))
        self.assertEqual(len(elems), 5)

        sections = self.get_sections(procedure_url)
        self.assertEqual(len(sections), 2)

        paragraphs = self.get_paragraphs(procedure_url)
        self.assertEqual(len(paragraphs), 1)

        steps = self.get_steps_generic(procedure_url)
        self.assertEqual(len(sections), 2)

        # get structure
        res_dict = self.get_structure(procedure_id)
        logger.debug('structure orig res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['children'][0]['children'][2]['description'], 'Step 1-3')
        self.assertEqual(res_dict['children'][0]['children'][2]['number'], '1-3')

        # move element
        res_dict = self.move_element(procedure_url, section_1_id, section_2_id, 'CHILD')

        self.assertEqual(len(res_dict['numbers']), 5)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_2_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1')        
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_1_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-1') 
        self.assertEqual(res_dict['numbers'][2]['elem_id'], paragraph_1_1_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '1-1-1')         
        self.assertEqual(res_dict['numbers'][3]['elem_id'], step_1_2_id)
        self.assertEqual(res_dict['numbers'][3]['number'], '1-1-2') 
        self.assertEqual(res_dict['numbers'][4]['elem_id'], step_1_3_id)
        self.assertEqual(res_dict['numbers'][4]['number'], '1-1-3') 

        self.assertEqual(len(res_dict['elem_ids']), 5)
        self.assertEqual(res_dict['elem_ids'][0], section_2_id)        
        self.assertEqual(res_dict['elem_ids'][1], section_1_id) 
        self.assertEqual(res_dict['elem_ids'][2], paragraph_1_1_id)
        self.assertEqual(res_dict['elem_ids'][3], step_1_2_id)        
        self.assertEqual(res_dict['elem_ids'][4], step_1_3_id) 


        res_dict = self.get_structure(procedure_id)

        logger.debug('structure moved res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['children'][0]['children'][0]['children'][2]['description'], 'Step 1-3')
        self.assertEqual(res_dict['children'][0]['children'][0]['children'][2]['number'], '1-1-3')

        # move it back
        self.move_element(procedure_url, section_1_id, '-1', 'CHILD')
        res_dict = self.get_structure(procedure_id)
        logger.debug('structure restored res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['children'][0]['children'][2]['description'], 'Step 1-3')
        self.assertEqual(res_dict['children'][0]['children'][2]['number'], '1-3')

        # delete elements
        res_dict = self.delete_element(procedure_url, paragraph_1_1_id)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 2)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_1_2_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-1') 
        self.assertEqual(res_dict['numbers'][1]['elem_id'], step_1_3_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-2')         

        self.assertEqual(len(res_dict['elem_ids']), 4)     
        self.assertEqual(res_dict['elem_ids'][0], section_1_id) 
        self.assertEqual(res_dict['elem_ids'][1], step_1_2_id)        
        self.assertEqual(res_dict['elem_ids'][2], step_1_3_id) 
        self.assertEqual(res_dict['elem_ids'][3], section_2_id)   

        res_dict = self.delete_element(procedure_url, step_1_2_id)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 1)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_1_3_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-1') 

        self.assertEqual(len(res_dict['elem_ids']), 3)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)         
        self.assertEqual(res_dict['elem_ids'][1], step_1_3_id) 
        self.assertEqual(res_dict['elem_ids'][2], section_2_id)  

        res_dict = self.delete_element(procedure_url, section_1_id)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))

        res_dict = self.delete_element(procedure_url, section_2_id)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))

        # get structure
        res_dict = self.get_structure(procedure_id)
        logger.debug('after deletion structure res_dict: %s', json.dumps(res_dict, indent=4))

        sections = self.get_sections(procedure_url)
        self.assertEqual(len(sections), 0)

        paragraphs = self.get_paragraphs(procedure_url)
        self.assertEqual(len(paragraphs), 0)

        steps = self.get_steps_generic(procedure_url)
        self.assertEqual(len(steps), 0)

    def test_move_element(self):
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']

        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section 1
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            title='Section 1')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Section 1-1')

        section_1_1 = res['elem']
        section_1_1_id = section_1_1['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_1_id,
            level='SIBLING',
            title='Section 1-2')

        section_1_2 = res['elem']
        section_1_2_id = section_1_2['elem_id']

        # Add section 2
        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='SIBLING',
            title='Section 2')

        section_2 = res['elem']
        section_2_id = section_2['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_2_id,
            level='CHILD',
            title='Section 2-1')

        section_2_1 = res['elem']
        section_2_1_id = section_2_1['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_2_1_id,
            level='SIBLING',
            title='Section 2-2')

        section_2_2 = res['elem']
        section_2_2_id = section_2_2['elem_id']
        
        # Cannot move to itself
        res_dict = self.move_element(procedure_url, section_1_1_id, section_1_1_id, 'CHILD', code_expected=400)
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['details']), 1)
        self.assertEqual(res_dict['details'][0], 'Cannot move an element to itself or its child')
        
        # Cannot move to itself
        res_dict = self.move_element(procedure_url, section_1_id, section_1_1_id, 'SIBLING', code_expected=400)
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['details']), 1)
        self.assertEqual(res_dict['details'][0], 'Cannot move an element to itself or its child')        
        
        # Cannot move to its child
        res_dict = self.move_element(procedure_url, section_1_id, section_1_1_id, 'CHILD', code_expected=400)
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['details']), 1)
        self.assertEqual(res_dict['details'][0], 'Cannot move an element to itself or its child')             

        structure_dict = self.get_structure(procedure_id=procedure_id)
        # logger.debug('orig structure_dict: %s', json.dumps(structure_dict, indent=4))

        res_dict = self.move_element(procedure_url, section_2_1_id, section_1_1_id, 'SIBLING')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 3)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-3')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '2-1')

        structure_dict = self.get_structure(procedure_id=procedure_id)
        logger.debug('moved structure_dict: %s', json.dumps(structure_dict, indent=4))

        self.assertEqual(structure_dict['children'][0]['title'], 'Section 1')
        self.assertEqual(structure_dict['children'][0]['number'], '1')
        self.assertEqual(structure_dict['children'][0]['children'][0]['title'], 'Section 1-1')
        self.assertEqual(structure_dict['children'][0]['children'][0]['number'], '1-1')
        self.assertEqual(structure_dict['children'][0]['children'][1]['title'], 'Section 2-1')
        self.assertEqual(structure_dict['children'][0]['children'][1]['number'], '1-2')
        self.assertEqual(structure_dict['children'][0]['children'][2]['title'], 'Section 1-2')
        self.assertEqual(structure_dict['children'][0]['children'][2]['number'], '1-3')
        self.assertEqual(structure_dict['children'][1]['title'], 'Section 2')
        self.assertEqual(structure_dict['children'][1]['number'], '2')
        self.assertEqual(structure_dict['children'][1]['children'][0]['title'], 'Section 2-2')
        self.assertEqual(structure_dict['children'][1]['children'][0]['number'], '2-1')

    def test_move_elements(self):
        id_dict = self.create_procedure_example()

        procedure_url = id_dict['procedure_url'] 
        procedure_id = id_dict['procedure_id']     
        version_id = id_dict['version_id']      
        section_1_id = id_dict['section_1_id'] 
        section_1_1_id = id_dict['section_1_1_id']    
        section_1_2_id = id_dict['section_1_2_id']    
        section_2_id = id_dict['section_2_id']
        section_2_1_id = id_dict['section_2_1_id']
        section_2_2_id = id_dict['section_2_2_id']  
        """
        1
          1-1
          1-2
        2
          2-1
          2-2
        """
        ## move element
        res_dict = self.move_elements(procedure_url, [section_2_1_id], section_1_1_id, 'SIBLING')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 3)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-3')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '2-1')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][3], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1
          1-1
          2-1*
          1-2*
        2
          2-2*
        """
        # restore
        res_dict = self.move_elements(procedure_url, [section_2_1_id], section_2_id, 'CHILD')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 3)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '2-2')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1
          1-1
          1-2*
        2
          2-1*
          2-2*
        """
        
        ## move element
        res_dict = self.move_elements(procedure_url, [section_2_1_id, section_2_2_id], section_1_1_id, 'SIBLING')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 3)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-3')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '1-4')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_id)

        elements = self.get_elements(procedure_url)
        logger.debug('after move elements elements= %s', json.dumps(elements, indent=4))   

        self.assertEqual(len(elements), 6)

        for element in elements:
            self.assertEqual(element['procedure_id'], procedure_id)
            self.assertEqual(element['version_id'], version_id)    

        self.assertEqual(elements[0]['number'], '1')
        self.assertEqual(elements[1]['number'], '1-1')
        self.assertEqual(elements[2]['number'], '1-2')
        self.assertEqual(elements[3]['number'], '1-3')
        self.assertEqual(elements[4]['number'], '1-4')
        self.assertEqual(elements[5]['number'], '2')

        self.assertEqual(elements[0]['elem_id'], section_1_id)
        self.assertEqual(elements[1]['elem_id'], section_1_1_id)
        self.assertEqual(elements[2]['elem_id'], section_2_1_id)
        self.assertEqual(elements[3]['elem_id'], section_2_2_id)
        self.assertEqual(elements[4]['elem_id'], section_1_2_id)
        self.assertEqual(elements[5]['elem_id'], section_2_id)

        """
        1
          1-1
          2-1*
          2-2*
          1-2*
        2
        """

        # restore
        res_dict = self.move_elements(procedure_url, [section_2_1_id, section_2_2_id], section_2_id, 'CHILD')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 3)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '2-2')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1
          1-1
          1-2*
        2
          2-1*
          2-2*
        """

        ## move elements
        res_dict = self.move_elements(procedure_url, [section_2_2_id, section_2_1_id], section_1_1_id, 'SIBLING')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 3)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-3')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '1-4')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_id)

        """
        1
          1-1
          2-1*
          2-2*
          1-2*
        2
        """

        # restore
        res_dict = self.move_elements(procedure_url, [section_2_2_id, section_2_1_id], section_2_id, 'CHILD')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 3)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '2-2')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1
          1-1
          1-2*
        2
          2-1*
          2-2*
        """

        ## move elements
        res_dict = self.move_elements(procedure_url, [section_1_1_id, section_2_1_id], section_1_2_id, 'SIBLING')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 4)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-1')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_1_1_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '1-3')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][3]['number'], '2-1')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)

        """
        1
          1-2*
          1-1*
          2-1*
        2
          2-2*
        """

        # restore 1/2
        res_dict = self.move_elements(procedure_url, [section_1_1_id], section_1_id, 'CHILD')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 2)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-1')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-2')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1
          1-1*
          1-2*
          2-1
        2
          2-2
        """

        # restore 2/2
        res_dict = self.move_elements(procedure_url, [section_2_1_id], section_2_id, 'CHILD')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 2)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '2-2')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1
          1-1
          1-2
        2
          2-1*
          2-2*
        """

        ## move elements
        res_dict = self.move_elements(procedure_url, [section_1_1_id, section_2_id], '-1', 'CHILD')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 6)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '2')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][3]['number'], '2-2')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], section_1_id)
        self.assertEqual(res_dict['numbers'][4]['number'], '3')
        self.assertEqual(res_dict['numbers'][5]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][5]['number'], '3-1')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_2_id)
        self.assertEqual(res_dict['elem_ids'][2], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_1_2_id)

        """
        1-1*
        2*
          2-1*
          2-2*
        1*
          1-2*
        """

        # restore 1/2
        res_dict = self.move_elements(procedure_url, [section_2_id], section_1_id, 'SIBLING')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 5)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '3')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][3]['number'], '3-1')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][4]['number'], '3-2')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1-1
        1*
          1-2*
        2*
          2-1*
          2-2*
        """

        # restore 2/2
        res_dict = self.move_elements(procedure_url, [section_1_1_id], section_1_id, 'CHILD')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 6)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_1_1_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-1')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], section_2_id)
        self.assertEqual(res_dict['numbers'][3]['number'], '2')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][4]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][5]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][5]['number'], '2-2')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1*
          1-1*
          1-2*
        2*
          2-1*
          2-2*
        """

        ## move elements (duplicated selections)
        res_dict = self.move_elements(procedure_url, [section_1_1_id, section_2_id, section_2_2_id], '-1', 'CHILD')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 6)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '2')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][3]['number'], '2-2')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], section_1_id)
        self.assertEqual(res_dict['numbers'][4]['number'], '3')
        self.assertEqual(res_dict['numbers'][5]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][5]['number'], '3-1')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_2_id)
        self.assertEqual(res_dict['elem_ids'][2], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_1_2_id)

        """
        1-1*
        2*
          2-1*
          2-2*
        1*
          1-2*
        """

        # restore 1/2
        res_dict = self.move_elements(procedure_url, [section_2_id], section_1_id, 'SIBLING')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 5)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '3')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][3]['number'], '3-1')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][4]['number'], '3-2')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1-1
        1*
          1-2*
        2*
          2-1*
          2-2*
        """

        # restore 2/2
        res_dict = self.move_elements(procedure_url, [section_1_1_id], section_1_id, 'CHILD')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 6)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_1_id)
        self.assertEqual(res_dict['numbers'][0]['number'], '1')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_1_1_id)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-1')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_1_2_id)
        self.assertEqual(res_dict['numbers'][2]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], section_2_id)
        self.assertEqual(res_dict['numbers'][3]['number'], '2')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], section_2_1_id)
        self.assertEqual(res_dict['numbers'][4]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][5]['elem_id'], section_2_2_id)
        self.assertEqual(res_dict['numbers'][5]['number'], '2-2')

        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][3], section_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_2_id)
        """
        1*
          1-1*
          1-2*
        2*
          2-1*
          2-2*
        """
                                           
    def create_procedure_example(self):
        id_dict = {}

        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']

        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section 1
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            title='Section 1')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Section 1-1')

        section_1_1 = res['elem']
        section_1_1_id = section_1_1['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_1_id,
            level='SIBLING',
            title='Section 1-2')

        section_1_2 = res['elem']
        section_1_2_id = section_1_2['elem_id']

        # Add section 2
        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='SIBLING',
            title='Section 2')

        section_2 = res['elem']
        section_2_id = section_2['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_2_id,
            level='CHILD',
            title='Section 2-1')

        section_2_1 = res['elem']
        section_2_1_id = section_2_1['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_2_1_id,
            level='SIBLING',
            title='Section 2-2')

        section_2_2 = res['elem']
        section_2_2_id = section_2_2['elem_id']

        id_dict['procedure_url'] = procedure_url
        id_dict['procedure_id'] = procedure_id     
        id_dict['version_id'] = section_1['version_id']               
        id_dict['section_1_id'] = section_1_id 
        id_dict['section_1_1_id'] = section_1_1_id    
        id_dict['section_1_2_id'] = section_1_2_id    
        id_dict['section_2_id'] = section_2_id 
        id_dict['section_2_1_id'] = section_2_1_id    
        id_dict['section_2_2_id'] = section_2_2_id                        

        return id_dict     
        
    def test_copy_element(self):
        id_dict = self.create_procedure_example()

        procedure_url = id_dict['procedure_url'] 
        procedure_id = id_dict['procedure_id']     
        version_id = id_dict['version_id']      
        section_1_id = id_dict['section_1_id'] 
        section_1_1_id = id_dict['section_1_1_id']    
        section_1_2_id = id_dict['section_1_2_id']    
        section_2_id = id_dict['section_2_id']
        section_2_1_id = id_dict['section_2_1_id']
        section_2_2_id = id_dict['section_2_2_id']  

        res_dict = self.copy_element(procedure_url, section_2_1_id, section_1_1_id, 'SIBLING')
        logger.debug('copy res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict['numbers']), 2)
        self.assertEqual(res_dict['numbers'][0]['number'], "1-2")
        self.assertEqual(res_dict['numbers'][1]['number'], "1-3")

        self.assertEqual(len(res_dict['elements']), 1)
        self.assertEqual(res_dict['elements'][0]['title'], 'Section 2-1')
        self.assertEqual(res_dict['elements'][0]['number'], '1-2')        

        self.assertEqual(len(res_dict['elem_ids']), 7)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], res_dict['elements'][0]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][3], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][6], section_2_2_id)                                              

        res_dict = self.get_version_elements(procedure_id=procedure_id, version=0)
        logger.debug('copied elements res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 7)
        self.assertEqual(res_dict[0]['title'], "Section 1")
        self.assertEqual(res_dict[1]['title'], "Section 1-1")
        self.assertEqual(res_dict[2]['title'], "Section 2-1")        
        self.assertEqual(res_dict[3]['title'], "Section 1-2")
        self.assertEqual(res_dict[4]['title'], "Section 2")
        self.assertEqual(res_dict[5]['title'], "Section 2-1")                        
        self.assertEqual(res_dict[6]['title'], "Section 2-2") 

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "1-3")
        self.assertEqual(res_dict[4]['number'], "2")
        self.assertEqual(res_dict[5]['number'], "2-1")
        self.assertEqual(res_dict[6]['number'], "2-2")

    def test_copy_element_across_procedures(self):
        logger.debug('test_copy_across_procedures')

        source_id_dict = self.create_procedure_example()
        source_procedure_url = source_id_dict['procedure_url']         
        source_procedure_id = source_id_dict['procedure_id']   
        source_version_id = source_id_dict['version_id']         
        source_section_1_id = source_id_dict['section_1_id'] 
        source_section_1_1_id = source_id_dict['section_1_1_id']    
        source_section_1_2_id = source_id_dict['section_1_2_id']    
        source_section_2_id = source_id_dict['section_2_id']
        source_section_2_1_id = source_id_dict['section_2_1_id']
        source_section_2_2_id = source_id_dict['section_2_2_id']  

        target_id_dict = self.create_procedure_example()
        target_procedure_url = target_id_dict['procedure_url']         
        target_procedure_id = target_id_dict['procedure_id']
        target_version_id = target_id_dict['version_id']           
        target_section_1_id = target_id_dict['section_1_id'] 
        target_section_1_1_id = target_id_dict['section_1_1_id']    
        target_section_1_2_id = target_id_dict['section_1_2_id']    
        target_section_2_id = target_id_dict['section_2_id']
        target_section_2_1_id = target_id_dict['section_2_1_id']
        target_section_2_2_id = target_id_dict['section_2_2_id']  

        self.assertNotEqual(source_version_id, target_version_id)

        res_dict = self.copy_element_across(target_procedure_url, source_section_1_id, target_section_1_id, 'SIBLING', 
            None, source_procedure_id, 0)
        logger.debug('element copied res_dict: %s', json.dumps(res_dict, indent=4))            

        added_elements = res_dict['elements']
        self.assertEqual(len(added_elements), 3)

        for added_element in added_elements:
            self.assertEqual(added_element['procedure_id'], target_procedure_id)

        numbers = res_dict['numbers']
        self.assertEqual(len(numbers), 6)

        self.assertEqual(numbers[0]['number'], '2')
        self.assertEqual(numbers[1]['number'], '2-1')
        self.assertEqual(numbers[2]['number'], '2-2')
        self.assertEqual(numbers[3]['number'], '3')
        self.assertEqual(numbers[4]['number'], '3-1')
        self.assertEqual(numbers[5]['number'], '3-2')        

        elements = self.get_elements(target_procedure_url)
        logger.debug('after copy elements elements= %s', json.dumps(elements, indent=4))   

        self.assertEqual(len(elements), 9)

        for element in elements:
            self.assertEqual(element['procedure_id'], target_procedure_id)
            self.assertEqual(element['version_id'], target_version_id)    

        self.assertEqual(elements[0]['number'], '1')
        self.assertEqual(elements[1]['number'], '1-1')
        self.assertEqual(elements[2]['number'], '1-2')
        self.assertEqual(elements[3]['number'], '2')
        self.assertEqual(elements[4]['number'], '2-1')
        self.assertEqual(elements[5]['number'], '2-2')
        self.assertEqual(elements[6]['number'], '3')
        self.assertEqual(elements[7]['number'], '3-1')
        self.assertEqual(elements[8]['number'], '3-2') 
        
        # Test the behavior of comment for copy operation

        # add version
        version_dict = self.create_procedure_version(source_procedure_id, 'First version', 'hongmank')
        self.assertEqual(version_dict['version'], 1)
        
        res_dict = self.get_version_elements(procedure_id=source_procedure_id, version=1)
        logger.debug('copied elements res_dict: %s', json.dumps(res_dict, indent=4))     
        
        source_section_id_v1_1 = res_dict[0]['elem_id']
        procedure_version_url = shared_dict['host'] + '/procedures/' + source_procedure_id + '/versions/1'
        logger.debug('procedure_version_url: %s', procedure_version_url)

        # only generic comment is allowed for procedure
        res_dict = self.add_conversation(procedure_version_url, source_section_id_v1_1, {'type': 'DATA_REVIEW_COMMENT'}, code_expected=400)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        
        # Add comment to section                
        content = 'This is the first comment for the section'
        res_dict = self.add_conversation(procedure_version_url, source_section_id_v1_1, {'type': 'COMMENT'})
        conversation_id = res_dict['conversation_id']
        comment = res_dict['comments'][0]
        comment_id = comment['comment_id']        
        res_dict = self.update_comment(procedure_version_url, source_section_id_v1_1, conversation_id, comment_id, content)
    
        # copy
        res_dict = self.copy_element_across(target_procedure_url, source_section_id_v1_1, '-1', 'CHILD', 
            None, source_procedure_id, 1)
        logger.debug('element copied res_dict: %s', json.dumps(res_dict, indent=4))  
        
        res_dict = self.get_version_elements(procedure_id=target_procedure_id, version=0)
        logger.debug('copied elements res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict[0]['conversations']), 0)
        self.assertEqual('comments' in res_dict[0], False)    
           

    def test_copy_elements(self):
        id_dict = self.create_procedure_example()

        procedure_url = id_dict['procedure_url'] 
        procedure_id = id_dict['procedure_id']     
        version_id = id_dict['version_id']      
        section_1_id = id_dict['section_1_id'] 
        section_1_1_id = id_dict['section_1_1_id']    
        section_1_2_id = id_dict['section_1_2_id']    
        section_2_id = id_dict['section_2_id']
        section_2_1_id = id_dict['section_2_1_id']
        section_2_2_id = id_dict['section_2_2_id']  

        ## copy element
        res_dict = self.copy_elements(procedure_url, [section_2_1_id], section_1_1_id, 'SIBLING')
        logger.debug('copy res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict['numbers']), 2)
        self.assertEqual(res_dict['numbers'][0]['number'], "1-2")
        self.assertEqual(res_dict['numbers'][1]['number'], "1-3")

        self.assertEqual(len(res_dict['elements']), 1)
        self.assertEqual(res_dict['elements'][0]['title'], 'Section 2-1')
        self.assertEqual(res_dict['elements'][0]['number'], '1-2')                

        copied_elem_infos = res_dict['elements']

        self.assertEqual(len(res_dict['elem_ids']), 7)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], copied_elem_infos[0]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][3], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][4], section_2_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][6], section_2_2_id)                                              

        res_dict = self.get_version_elements(procedure_id=procedure_id, version=0)
        logger.debug('copied elements res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 7)
        self.assertEqual(res_dict[0]['title'], "Section 1")
        self.assertEqual(res_dict[1]['title'], "Section 1-1")
        self.assertEqual(res_dict[2]['title'], "Section 2-1")        
        self.assertEqual(res_dict[3]['title'], "Section 1-2")
        self.assertEqual(res_dict[4]['title'], "Section 2")
        self.assertEqual(res_dict[5]['title'], "Section 2-1")                        
        self.assertEqual(res_dict[6]['title'], "Section 2-2") 

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "1-3")
        self.assertEqual(res_dict[4]['number'], "2")
        self.assertEqual(res_dict[5]['number'], "2-1")
        self.assertEqual(res_dict[6]['number'], "2-2")

        # reset
        for copied_elem_info in copied_elem_infos:
            self.delete_element(procedure_url, copied_elem_info['elem_id'], code_expected=200)

        ## copy two elements 
        res_dict = self.copy_elements(procedure_url, [section_2_1_id, section_2_2_id], section_1_1_id, 'SIBLING')
        logger.debug('copy res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict['numbers']), 3)
        self.assertEqual(res_dict['numbers'][0]['number'], "1-2")
        self.assertEqual(res_dict['numbers'][1]['number'], "1-3")
        self.assertEqual(res_dict['numbers'][2]['number'], "1-4")

        self.assertEqual(len(res_dict['elements']), 2)
        self.assertEqual(res_dict['elements'][0]['title'], 'Section 2-1')
        self.assertEqual(res_dict['elements'][0]['number'], '1-2')       
        self.assertEqual(res_dict['elements'][1]['title'], 'Section 2-2')
        self.assertEqual(res_dict['elements'][1]['number'], '1-3')  

        copied_elem_infos = res_dict['elements']

        self.assertEqual(len(res_dict['elem_ids']), 8)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], copied_elem_infos[0]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][3], copied_elem_infos[1]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][4], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][5], section_2_id)
        self.assertEqual(res_dict['elem_ids'][6], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][7], section_2_2_id)                                              

        res_dict = self.get_version_elements(procedure_id=procedure_id, version=0)
        logger.debug('copied elements res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 8)
        self.assertEqual(res_dict[0]['title'], "Section 1")
        self.assertEqual(res_dict[1]['title'], "Section 1-1")
        self.assertEqual(res_dict[2]['title'], "Section 2-1")    
        self.assertEqual(res_dict[3]['title'], "Section 2-2")    
        self.assertEqual(res_dict[4]['title'], "Section 1-2")
        self.assertEqual(res_dict[5]['title'], "Section 2")
        self.assertEqual(res_dict[6]['title'], "Section 2-1")                        
        self.assertEqual(res_dict[7]['title'], "Section 2-2") 

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "1-3")
        self.assertEqual(res_dict[4]['number'], "1-4")
        self.assertEqual(res_dict[5]['number'], "2")
        self.assertEqual(res_dict[6]['number'], "2-1")
        self.assertEqual(res_dict[7]['number'], "2-2")

        # reset
        for copied_elem_info in copied_elem_infos:
            self.delete_element(procedure_url, copied_elem_info['elem_id'], code_expected=200)

        ## copy elements in the same parent
        res_dict = self.copy_elements(procedure_url, [section_2_id, section_2_1_id, section_2_2_id], section_1_1_id, 'SIBLING')
        logger.debug('copy res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict['numbers']), 4)
        self.assertEqual(res_dict['numbers'][0]['number'], "1-2")
        self.assertEqual(res_dict['numbers'][1]['number'], "1-2-1")
        self.assertEqual(res_dict['numbers'][2]['number'], "1-2-2")
        self.assertEqual(res_dict['numbers'][3]['number'], "1-3")

        self.assertEqual(len(res_dict['elements']), 3)
        self.assertEqual(res_dict['elements'][0]['title'], 'Section 2')
        self.assertEqual(res_dict['elements'][0]['number'], '1-2')        
        self.assertEqual(res_dict['elements'][1]['title'], 'Section 2-1')
        self.assertEqual(res_dict['elements'][1]['number'], '1-2-1')       
        self.assertEqual(res_dict['elements'][2]['title'], 'Section 2-2')
        self.assertEqual(res_dict['elements'][2]['number'], '1-2-2')  

        copied_elem_infos = res_dict['elements']

        self.assertEqual(len(res_dict['elem_ids']), 9)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], copied_elem_infos[0]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][3], copied_elem_infos[1]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][4], copied_elem_infos[2]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][5], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][6], section_2_id)
        self.assertEqual(res_dict['elem_ids'][7], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][8], section_2_2_id)                                              

        res_dict = self.get_version_elements(procedure_id=procedure_id, version=0)
        logger.debug('copied elements res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 9)
        self.assertEqual(res_dict[0]['title'], "Section 1")
        self.assertEqual(res_dict[1]['title'], "Section 1-1")
        self.assertEqual(res_dict[2]['title'], "Section 2")
        self.assertEqual(res_dict[3]['title'], "Section 2-1")    
        self.assertEqual(res_dict[4]['title'], "Section 2-2")    
        self.assertEqual(res_dict[5]['title'], "Section 1-2")
        self.assertEqual(res_dict[6]['title'], "Section 2")
        self.assertEqual(res_dict[7]['title'], "Section 2-1")                        
        self.assertEqual(res_dict[8]['title'], "Section 2-2") 

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "1-2-1")
        self.assertEqual(res_dict[4]['number'], "1-2-2")
        self.assertEqual(res_dict[5]['number'], "1-3")
        self.assertEqual(res_dict[6]['number'], "2")
        self.assertEqual(res_dict[7]['number'], "2-1")
        self.assertEqual(res_dict[8]['number'], "2-2")

        # reset
        self.delete_element(procedure_url, copied_elem_infos[0]['elem_id'], code_expected=200)

        ## copy elements in the same parent (not in order)
        res_dict = self.copy_elements(procedure_url, [section_2_1_id, section_2_2_id, section_2_id], section_1_1_id, 'SIBLING')
        logger.debug('copy res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict['numbers']), 4)
        self.assertEqual(res_dict['numbers'][0]['number'], "1-2")
        self.assertEqual(res_dict['numbers'][1]['number'], "1-2-1")
        self.assertEqual(res_dict['numbers'][2]['number'], "1-2-2")
        self.assertEqual(res_dict['numbers'][3]['number'], "1-3")

        self.assertEqual(len(res_dict['elements']), 3)
        self.assertEqual(res_dict['elements'][0]['title'], 'Section 2')
        self.assertEqual(res_dict['elements'][0]['number'], '1-2')        
        self.assertEqual(res_dict['elements'][1]['title'], 'Section 2-1')
        self.assertEqual(res_dict['elements'][1]['number'], '1-2-1')       
        self.assertEqual(res_dict['elements'][2]['title'], 'Section 2-2')
        self.assertEqual(res_dict['elements'][2]['number'], '1-2-2')  

        copied_elem_infos = res_dict['elements']

        self.assertEqual(len(res_dict['elem_ids']), 9)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], copied_elem_infos[0]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][3], copied_elem_infos[1]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][4], copied_elem_infos[2]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][5], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][6], section_2_id)
        self.assertEqual(res_dict['elem_ids'][7], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][8], section_2_2_id)                                              

        res_dict = self.get_version_elements(procedure_id=procedure_id, version=0)
        logger.debug('copied elements res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 9)
        self.assertEqual(res_dict[0]['title'], "Section 1")
        self.assertEqual(res_dict[1]['title'], "Section 1-1")
        self.assertEqual(res_dict[2]['title'], "Section 2")
        self.assertEqual(res_dict[3]['title'], "Section 2-1")    
        self.assertEqual(res_dict[4]['title'], "Section 2-2")    
        self.assertEqual(res_dict[5]['title'], "Section 1-2")
        self.assertEqual(res_dict[6]['title'], "Section 2")
        self.assertEqual(res_dict[7]['title'], "Section 2-1")                        
        self.assertEqual(res_dict[8]['title'], "Section 2-2") 

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "1-2-1")
        self.assertEqual(res_dict[4]['number'], "1-2-2")
        self.assertEqual(res_dict[5]['number'], "1-3")
        self.assertEqual(res_dict[6]['number'], "2")
        self.assertEqual(res_dict[7]['number'], "2-1")
        self.assertEqual(res_dict[8]['number'], "2-2")

        # reset
        self.delete_element(procedure_url, copied_elem_infos[0]['elem_id'], code_expected=200)        

        ## copy elements in the different parents
        res_dict = self.copy_elements(procedure_url, [section_1_2_id, section_2_id], section_1_1_id, 'SIBLING')
        logger.debug('copy res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict['numbers']), 5)
        self.assertEqual(res_dict['numbers'][0]['number'], "1-2")
        self.assertEqual(res_dict['numbers'][1]['number'], "1-3")
        self.assertEqual(res_dict['numbers'][2]['number'], "1-3-1")
        self.assertEqual(res_dict['numbers'][3]['number'], "1-3-2")
        self.assertEqual(res_dict['numbers'][4]['number'], "1-4")

        self.assertEqual(len(res_dict['elements']), 4)
        self.assertEqual(res_dict['elements'][0]['title'], 'Section 1-2')
        self.assertEqual(res_dict['elements'][0]['number'], '1-2')
        self.assertEqual(res_dict['elements'][1]['title'], 'Section 2')
        self.assertEqual(res_dict['elements'][1]['number'], '1-3')        
        self.assertEqual(res_dict['elements'][2]['title'], 'Section 2-1')
        self.assertEqual(res_dict['elements'][2]['number'], '1-3-1')       
        self.assertEqual(res_dict['elements'][3]['title'], 'Section 2-2')
        self.assertEqual(res_dict['elements'][3]['number'], '1-3-2')  

        copied_elem_infos = res_dict['elements']

        self.assertEqual(len(res_dict['elem_ids']), 10)
        self.assertEqual(res_dict['elem_ids'][0], section_1_id)
        self.assertEqual(res_dict['elem_ids'][1], section_1_1_id)
        self.assertEqual(res_dict['elem_ids'][2], copied_elem_infos[0]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][3], copied_elem_infos[1]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][4], copied_elem_infos[2]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][5], copied_elem_infos[3]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][6], section_1_2_id)
        self.assertEqual(res_dict['elem_ids'][7], section_2_id)
        self.assertEqual(res_dict['elem_ids'][8], section_2_1_id)
        self.assertEqual(res_dict['elem_ids'][9], section_2_2_id)                                              

        res_dict = self.get_version_elements(procedure_id=procedure_id, version=0)
        logger.debug('copied elements res_dict: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 10)
        self.assertEqual(res_dict[0]['title'], "Section 1")
        self.assertEqual(res_dict[1]['title'], "Section 1-1")
        self.assertEqual(res_dict[2]['title'], "Section 1-2")
        self.assertEqual(res_dict[3]['title'], "Section 2")
        self.assertEqual(res_dict[4]['title'], "Section 2-1")    
        self.assertEqual(res_dict[5]['title'], "Section 2-2")    
        self.assertEqual(res_dict[6]['title'], "Section 1-2")
        self.assertEqual(res_dict[7]['title'], "Section 2")
        self.assertEqual(res_dict[8]['title'], "Section 2-1")                        
        self.assertEqual(res_dict[9]['title'], "Section 2-2") 

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "1-3")
        self.assertEqual(res_dict[4]['number'], "1-3-1")
        self.assertEqual(res_dict[5]['number'], "1-3-2")
        self.assertEqual(res_dict[6]['number'], "1-4")
        self.assertEqual(res_dict[7]['number'], "2")
        self.assertEqual(res_dict[8]['number'], "2-1")
        self.assertEqual(res_dict[9]['number'], "2-2")

        # reset
        self.delete_element(procedure_url, copied_elem_infos[0]['elem_id'], code_expected=200)
        self.delete_element(procedure_url, copied_elem_infos[1]['elem_id'], code_expected=200)              

    def test_copy_elements_across_procedures(self):
        logger.debug('test_copy_across_procedures')

        source_id_dict = self.create_procedure_example()
        source_procedure_url = source_id_dict['procedure_url']         
        source_procedure_id = source_id_dict['procedure_id']   
        source_version_id = source_id_dict['version_id']         
        source_section_1_id = source_id_dict['section_1_id'] 
        source_section_1_1_id = source_id_dict['section_1_1_id']    
        source_section_1_2_id = source_id_dict['section_1_2_id']    
        source_section_2_id = source_id_dict['section_2_id']
        source_section_2_1_id = source_id_dict['section_2_1_id']
        source_section_2_2_id = source_id_dict['section_2_2_id']  

        target_id_dict = self.create_procedure_example()
        target_procedure_url = target_id_dict['procedure_url']         
        target_procedure_id = target_id_dict['procedure_id']
        target_version_id = target_id_dict['version_id']           
        target_section_1_id = target_id_dict['section_1_id'] 
        target_section_1_1_id = target_id_dict['section_1_1_id']    
        target_section_1_2_id = target_id_dict['section_1_2_id']    
        target_section_2_id = target_id_dict['section_2_id']
        target_section_2_1_id = target_id_dict['section_2_1_id']
        target_section_2_2_id = target_id_dict['section_2_2_id']  

        self.assertNotEqual(source_version_id, target_version_id)

        res_dict = self.copy_elements_across(target_procedure_url, [source_section_1_2_id, source_section_2_id], target_section_1_id, 'SIBLING', 
            None, source_procedure_id, 0)
        logger.debug('element copied res_dict: %s', json.dumps(res_dict, indent=4))            

        added_elements = res_dict['elements']
        self.assertEqual(len(added_elements), 4)

        for added_element in added_elements:
            self.assertEqual(added_element['procedure_id'], target_procedure_id)

        numbers = res_dict['numbers']
        self.assertEqual(len(numbers), 7)

        self.assertEqual(numbers[0]['number'], '2')
        self.assertEqual(numbers[1]['number'], '3')
        self.assertEqual(numbers[2]['number'], '3-1')
        self.assertEqual(numbers[3]['number'], '3-2')
        self.assertEqual(numbers[4]['number'], '4')
        self.assertEqual(numbers[5]['number'], '4-1')
        self.assertEqual(numbers[6]['number'], '4-2')        

        elements = self.get_elements(target_procedure_url)
        logger.debug('after copy elements elements= %s', json.dumps(elements, indent=4))   

        self.assertEqual(len(elements), 10)

        for element in elements:
            self.assertEqual(element['procedure_id'], target_procedure_id)
            self.assertEqual(element['version_id'], target_version_id)    

        self.assertEqual(elements[0]['number'], '1')
        self.assertEqual(elements[1]['number'], '1-1')
        self.assertEqual(elements[2]['number'], '1-2')
        self.assertEqual(elements[3]['number'], '2')
        self.assertEqual(elements[4]['number'], '3')
        self.assertEqual(elements[5]['number'], '3-1')
        self.assertEqual(elements[6]['number'], '3-2')
        self.assertEqual(elements[7]['number'], '4')
        self.assertEqual(elements[8]['number'], '4-1')
        self.assertEqual(elements[9]['number'], '4-2') 

    def test_get_procedure_versions(self):
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')
        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        rand_1 = random_string()
        description_1 = 'description_' + rand_1
        institutional_release_id_1 = 'institutional_release_id_1_' + rand_1
        self.create_procedure_version(procedure_id, description_1, 'hongmank')
        self.update_procedure_version(procedure_id, 1, {'institutional_release_id': institutional_release_id_1})
        self.update_procedure_version_status(procedure_id, 1, {'action': 'RELEASE'})

        rand_2 = random_string()
        description_2 = 'description_' + rand_2
        institutional_release_id_2 = 'institutional_release_id_2_' + rand_2
        author_2 = 'author_' + rand_2
        self.create_procedure_version(procedure_id, description_2, author_2)
        self.update_procedure_version(procedure_id, 2, {'institutional_release_id': institutional_release_id_2})
        self.update_procedure_version_status(procedure_id, 2, {'action': 'RELEASE'})

        rand_3 = random_string()
        description_3 = 'description_' + rand_3
        institutional_release_id_3 = 'institutional_release_id_3_' + rand_3
        self.create_procedure_version(procedure_id, description_3, 'hongmank')
        self.update_procedure_version(procedure_id, 3, {'institutional_release_id': institutional_release_id_3})
        self.update_procedure_version_status(procedure_id, 3, {'action': 'RELEASE'})

        self.update_procedure_version(procedure_id, 0, {'flight_dictionary_version': 'v2', 'sse_dictionary_version': 'v2.1'})

        rand_4 = random_string()
        description_4 = 'description_' + rand_4
        institutional_release_id_4 = 'institutional_release_id_4_' + rand_4
        self.create_procedure_version(procedure_id, description_4, 'hongmank')
        self.update_procedure_version(procedure_id, 4, {'institutional_release_id': institutional_release_id_4})
        self.update_procedure_version_status(procedure_id, 4, {'action': 'RELEASE'})

        # test if the meta data of working version is copied over
        version_dict = self.get_procedure_version(procedure_id, 4)
        self.assertEqual(version_dict['flight_dictionary_version'], 'v2')
        self.assertEqual(version_dict['sse_dictionary_version'], 'v2.1')

        url = '{0}/procedures/{1}/versions'.format(shared_dict['host'], procedure_id)
        params = {'limit': 10000}
        result = requests.get(url, headers=shared_dict['headers'])
        logger.debug(result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('versions: %s', json.dumps(res_dict, indent=4))
        venue_count = len(res_dict)
        self.assertGreater(len(res_dict), 4)    # including the working copy

        # check for the default sort
        self.assertEqual(res_dict[0]['version_description'], description_4)

        # filter by title
        params = {'version_description': rand_1}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['version_description'], description_1)

        # filter by author
        params = {'version_author': rand_2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['version_author'], author_2)

        # filter by institutional_release_id
        params = {'institutional_release_id': rand_2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['version_description'], description_2)

        # filter by versioned
        params = {'status': 'VERSIONED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('versions: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 0)
        
        # filter by submitted
        params = {'status': 'SUBMITTED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('versions: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 0)

        # filter by approved
        params = {'status': 'APPROVED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('versions: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 0)

        # filter by released
        params = {'status': 'RELEASED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 4)

        self.update_procedure_version_status(procedure_id, 4, {'action': 'UNRELEASE'})

        params = {'status': 'RELEASED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 3)

        self.update_procedure_version(procedure_id, 4, {'institutional_release_id': 'r4'})
        self.update_procedure_version_status(procedure_id, 4, {'action': 'RELEASE'})

        params = {'status': 'RELEASED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 4)

        # filter by obsolete
        params = {'status': 'OBSOLETE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 0)


        self.update_procedure_version_status(procedure_id, 3, {'action': 'OBSOLETE'})

        params = {'status': 'OBSOLETE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)


        self.update_procedure_version_status(procedure_id, 3, {'action': 'UNOBSOLETE'})

        params = {'status': 'OBSOLETE'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 0)

        # check for the sort
        params = {'limit': 10000, 'procedure_id': procedure_id, 'sort': 'DESC'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[0]['version_description'], description_4)

        params = {'limit': 10000, 'procedure_id': procedure_id, 'sort': 'ASC'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[-1]['version_description'], description_4)
        self.assertEqual(res_dict[-2]['version_description'], description_3)
        self.assertEqual(res_dict[-3]['version_description'], description_2)
        self.assertEqual(res_dict[-4]['version_description'], description_1)

        params = {'limit': 10000, 'procedure_id': procedure_id, 'sort': 'ASC', 'sort_by': 'TIME_VERSIONED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[-1]['version_description'], description_4)
        self.assertEqual(res_dict[-2]['version_description'], description_3)
        self.assertEqual(res_dict[-3]['version_description'], description_2)
        self.assertEqual(res_dict[-4]['version_description'], description_1)
        self.assertEqual(res_dict[-5]['version_description'], 'Working Version')

        params = {'limit': 10000, 'procedure_id': procedure_id, 'sort': 'DESC', 'sort_by': 'TIME_VERSIONED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[-1]['version_description'], 'Working Version')
        self.assertEqual(res_dict[-2]['version_description'], description_1)
        self.assertEqual(res_dict[-3]['version_description'], description_2)
        self.assertEqual(res_dict[-4]['version_description'], description_3)
        self.assertEqual(res_dict[-5]['version_description'], description_4)
        total_count = len(res_dict)

        params = {'limit': 10000, 'procedure_id': procedure_id, 'sort': 'ASC', 'sort_by': 'INSTITUTIONAL_RELEASE_ID'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict[-1]['version_description'], description_4)
        self.assertEqual(res_dict[-2]['version_description'], description_3)
        self.assertEqual(res_dict[-3]['version_description'], description_2)
        self.assertEqual(res_dict[-4]['version_description'], description_1)
        self.assertEqual(res_dict[-5]['version_description'], 'Working Version')

        params = {'limit': 10000, 'procedure_id': procedure_id, 'sort': 'ASC', 'sort_by': 'VERSION'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 5)

        params = {'limit': 10000, 'procedure_id': procedure_id, 'sort': 'ASC', 'sort_by': 'API_VERSION'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 5)

        params = {'limit': 10000, 'procedure_id': procedure_id, 'sort': 'ASC', 'sort_by': 'FLIGHT_DICTIONARY_VERSION'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 5)

        params = {'limit': 10000, 'procedure_id': procedure_id, 'sort': 'ASC', 'sort_by': 'SSE_DICTIONARY_VERSION'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 5)


        # offset and limit

        params = {'limit': 2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), total_count)

        params = {'offset': 1, 'limit': 2}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(int(result.headers['x-total-count']), total_count)
        self.assertEqual(res_dict[0]['version_description'], description_3)
        self.assertEqual(res_dict[1]['version_description'], description_2)

    def test_time_saved(self):
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']

        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        procedure_dict = self.get_procedure(procedure_id)
        time_saved_0 = procedure_dict['time_saved']

        logger.debug('procedure_dict: %s', json.dumps(procedure_dict, indent=4))
        self.assertGreater(len(time_saved_0), 0)

        # update procedure meta data
        self.update_procedure(procedure_id, {'description': 'new description'})
        procedure_dict = self.get_procedure(procedure_id)
        time_saved_1 = procedure_dict['time_saved']
        self.assertGreater(time_saved_1, time_saved_0)


        # Add section 1
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1')

        procedure_dict = self.get_procedure(procedure_id)
        time_saved_2 = procedure_dict['time_saved']
        self.assertGreater(time_saved_2, time_saved_1)

        # create version 1
        version_dict = self.create_procedure_version(procedure_id, 'version with a section', '')
        version = version_dict['version']
        time_saved_version_0 = version_dict['time_saved']
        self.assertGreater(len(time_saved_version_0), 0)

        procedure_dict = self.get_procedure(procedure_id)
        time_saved_3 = procedure_dict['time_saved']
        self.assertGreater(time_saved_3, time_saved_2)
        current_version = procedure_dict['current_version']
        self.assertEqual(current_version, 1)

        # create version 2
        version_dict = self.create_procedure_version(procedure_id, 'version with a section', '')
        version = version_dict['version']
        time_saved_version_1 = version_dict['time_saved']
        self.assertGreater(len(time_saved_version_1), 0)

        procedure_dict = self.get_procedure(procedure_id)
        time_saved_3 = procedure_dict['time_saved']
        self.assertGreater(time_saved_3, time_saved_2)
        current_version = procedure_dict['current_version']
        self.assertEqual(current_version, 2)


        # time_saved should be updated for procedure
        procedure_dict = self.get_procedure(procedure_id)
        time_saved_3 = procedure_dict['time_saved']
        self.assertGreater(time_saved_3, time_saved_2)

        # update version meta data
        self.update_procedure_version(procedure_id, version, {'version_description': 'new version description'})
        version_dict = self.get_procedure_version(procedure_id, version)
        logger.debug('version_dict: %s', json.dumps(version_dict, indent=4))
        time_saved_version_2 = version_dict['time_saved']
        self.assertGreater(time_saved_version_2, time_saved_version_1)

        ## delete version 2
        self.delete_procedure_version(procedure_id, 2)

        ## cannot delete working copy
        self.delete_procedure_version(procedure_id, 0, 400)

        # time_saved should be updated for procedure
        procedure_dict = self.get_procedure(procedure_id)
        time_saved_4 = procedure_dict['time_saved']
        self.assertGreater(time_saved_4, time_saved_3)

        # current_version should stay at 2
        current_version = procedure_dict['current_version']
        self.assertEqual(current_version, 2)

        ## obsolste version 1

        data = {'action': 'OBSOLETE'}
        res_dict = self.update_procedure_version_status(procedure_id, 1, data)
        self.assertEqual(res_dict['status'], 'OBSOLETE')

        # time_saved should not be updated for procedure
        procedure_dict = self.get_procedure(procedure_id)
        time_saved_5 = procedure_dict['time_saved']
        self.assertEqual(time_saved_5, time_saved_4)

        # current_version should be back to 0
        current_version = procedure_dict['current_version']
        self.assertEqual(current_version, 0)

    def test_procedure_version_status(self):
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')
        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        rand_1 = random_string()
        description_1 = 'description_' + rand_1
        institutional_release_id_1 = 'institutional_release_id_1_' + rand_1
        self.create_procedure_version(procedure_id, description_1, 'hongmank')

        # test if the meta data of working version is copied over
        version_dict = self.get_procedure_version(procedure_id, 1)
        version = version_dict['version']
        self.assertEqual(version_dict['status'], 'VERSIONED')

        # submit
        data = {'action': 'SUBMIT'}
        res_dict = self.update_procedure_version_status(procedure_id, version, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertEqual(res_dict['time_approved'], '')  
        self.assertEqual(res_dict['time_released'], '')  
        self.assertEqual(res_dict['institutional_release_id'], '')
        self.assertEqual(res_dict['status'], 'SUBMITTED')
        
        # approve
        data = {'action': 'APPROVE'}
        res_dict = self.update_procedure_version_status(procedure_id, version, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertTrue(len(res_dict['time_approved']) > 0)
        self.assertEqual(res_dict['time_released'], '')  
        self.assertEqual(res_dict['institutional_release_id'], '')
        self.assertEqual(res_dict['status'], 'APPROVED')

        # release
        res_dict = self.update_procedure_version(procedure_id, version, {'institutional_release_id': 'Initial Release'})
        data = {'action': 'RELEASE'}
        res_dict = self.update_procedure_version_status(procedure_id, version, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertTrue(len(res_dict['time_approved']) > 0)
        self.assertTrue(len(res_dict['time_released']) > 0)
        self.assertEqual(res_dict['institutional_release_id'], 'Initial Release')
        self.assertEqual(res_dict['status'], 'RELEASED')
        
        # obsolete
        data = {'action': 'OBSOLETE'}
        res_dict = self.update_procedure_version_status(procedure_id, version, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertTrue(len(res_dict['time_approved']) > 0)
        self.assertTrue(len(res_dict['time_released']) > 0)
        self.assertEqual(res_dict['institutional_release_id'], 'Initial Release')
        self.assertEqual(res_dict['status'], 'OBSOLETE')        
        
        # unobsolete
        data = {'action': 'UNOBSOLETE'}
        res_dict = self.update_procedure_version_status(procedure_id, version, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertTrue(len(res_dict['time_approved']) > 0)
        self.assertTrue(len(res_dict['time_released']) > 0)
        self.assertEqual(res_dict['status'], 'RELEASED')
        
        # unrelease
        data = {'action': 'UNRELEASE'}
        res_dict = self.update_procedure_version_status(procedure_id, version, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertTrue(len(res_dict['time_approved']) > 0)
        self.assertEqual(res_dict['time_released'], '')  
        self.assertEqual(res_dict['institutional_release_id'], 'Initial Release')
        self.assertEqual(res_dict['status'], 'APPROVED')

        # unapprove
        data = {'action': 'UNAPPROVE'}
        res_dict = self.update_procedure_version_status(procedure_id, version, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertEqual(res_dict['time_approved'], '')
        self.assertEqual(res_dict['time_released'], '')  
        self.assertEqual(res_dict['institutional_release_id'], 'Initial Release')
        self.assertEqual(res_dict['status'], 'SUBMITTED')

        # unsubmit
        data = {'action': 'UNSUBMIT'}
        res_dict = self.update_procedure_version_status(procedure_id, version, data)
        self.assertEqual(res_dict['time_submitted'], '') 
        self.assertEqual(res_dict['time_approved'], '')  
        self.assertEqual(res_dict['time_released'], '')  
        self.assertEqual(res_dict['institutional_release_id'], 'Initial Release')
        self.assertEqual(res_dict['status'], 'VERSIONED')
        
    def test_procedure_sections(self):
        rand = random_string()
        title = 'title_' + rand
        procedure_dict = self.create_procedure(title, 'Test procedure', '', 'hongmank')
        procedure_id_1 = procedure_dict['procedure_id']
        procedure_url_1 = shared_dict['host'] + '/procedures/' + procedure_id_1

        rand = random_string()
        description = 'description_' + rand
        version_dict_1 = self.create_procedure_version(procedure_id_1, description, 'hongmank')
        self.assertEqual(version_dict_1['version'], 1)

        rand = random_string()
        title = 'title_' + rand
        procedure_dict = self.create_procedure(title, 'Test procedure', '', 'hongmank')
        procedure_id_2 = procedure_dict['procedure_id']
        procedure_url_2 = shared_dict['host'] + '/procedures/' + procedure_id_2

        rand = random_string()
        description = 'description_' + rand
        version_dict_2 = self.create_procedure_version(procedure_id_2, description, 'hongmank')
        self.assertEqual(version_dict_2['version'], 1)

        rand = random_string()
        title = 'title_' + rand
        procedure_dict = self.create_procedure(title, 'Test procedure', '', 'hongmank')
        procedure_id_3 = procedure_dict['procedure_id']
        procedure_url_3 = shared_dict['host'] + '/procedures/' + procedure_id_3

        procedure_section_data_1 = {'elem_type': 'PROCEDURE_SECTION', 'description': "this is a description", 'title': 'this is a section title'}
        res = self.add_procedure_section(base_url=procedure_url_3,
            insert_after_id="-1",
            level='CHILD',
            procedure_section=procedure_section_data_1)

        procedure_section_1_id = res['elem']['elem_id']
        procedure_section_1 = self.get_procedure_section(procedure_url_3, procedure_section_1_id)

        self.assertEqual(procedure_section_1['title'], procedure_section_data_1['title'])

        # try to add an element to a procedure section (not allowed during authoring)
        res = self.add_section(base_url=procedure_url_3,
            insert_after_id=procedure_section_1_id,
            level='CHILD',
            description='Section that is not be allowed',
            code_expected=400)

        procedure_section_data_2 = {'elem_type': 'PROCEDURE_SECTION', 'description': "this is a description", 'title': 'this is a section title'}
        res = self.add_procedure_section(base_url=procedure_url_3,
            insert_after_id=procedure_section_1_id,
            level='SIBLING',
            procedure_section=procedure_section_data_2)

        procedure_sections = self.get_procedure_sections(procedure_url_3)
        self.assertEqual(len(procedure_sections), 2)


        procedure_section_update = {'description': "this is a NEW description"}
        self.update_procedure_section(procedure_url_3, procedure_section_1_id, procedure_section_update)

        procedure_section_1 = self.get_procedure_section(procedure_url_3, procedure_section_1_id)
        self.assertEqual(procedure_section_1['title'], procedure_section_data_1['title'])
        self.assertEqual(procedure_section_1['description'], procedure_section_update['description'])

        outline_elems = self.get_outline(procedure_url_2, 1)

        # input test
        procedure_section_input = {
            'reference_procedure_id': procedure_id_2,
            'reference_procedure_version': 1,
            'elements': outline_elems,
            'reference_procedure_version_description': '',
            'reference_procedure_title': ''  
        }

        self.update_procedure_section_input(procedure_url_3, procedure_section_1_id, procedure_section_input)

        user_input = self.get_procedure_section_input(procedure_url_3, procedure_section_1_id)

        self.assertDictEqual(procedure_section_input, user_input)
        #
        self.delete_element(procedure_url_3, procedure_section_1_id, code_expected=200)

        procedure_sections = self.get_procedure_sections(procedure_url_3)
        self.assertEqual(len(procedure_sections), 1)

    def test_procedure_version(self):
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='CHILD',
            description='Paragraph A')

        paragraph_a = res['elem']
        paragraph_a_id = paragraph_a['elem_id']

        # add step
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Step 1-1',
            description='Step 1-1')

        step_1_1 = res['elem']
        step_1_1_id = step_1_1['elem_id']

        # add version
        version_dict = self.create_procedure_version(procedure_id, 'First version', 'hongmank')
        self.assertEqual(version_dict['version'], 1)

        # add another version
        version_dict = self.create_procedure_version(procedure_id, 'Second version', 'hongmank')
        self.assertEqual(version_dict['version'], 2)

        # check version 1
        version_dict_1 = self.get_procedure_version(procedure_id, 1)
        self.assertEqual(version_dict_1['version'], 1)

        structure_version_1 = self.get_version_structure(procedure_id, 1)
        logger.debug('structure_version_1: %s', json.dumps(structure_version_1, indent=4))
        self.assertEqual(structure_version_1['children'][0]['children'][0]['description'], 'Step 1-1')
        self.assertEqual(structure_version_1['children'][0]['children'][0]['number'], '1-1')
        self.assertEqual(structure_version_1['children'][0]['children'][1]['description'], 'Paragraph A')

        elements_version_1 = self.get_version_elements(procedure_id, 1)
        self.assertEqual(len(elements_version_1), 3)
        self.assertEqual(elements_version_1[0]['number'], '1')
        self.assertEqual(elements_version_1[1]['number'], '1-1')
        
        # Cannot modify a versioned element
        res_dict = self.update_element(procedure_url, elements_version_1[1]['elem_id'], {'title': 'modified title'}, code_expected=400)
        self.assertEqual(res_dict['details'][0], 'Cannot modify element of versioned procedure')
                
        # Cannot delete a versioned element
        res_dict = self.delete_element(procedure_url, elements_version_1[1]['elem_id'], code_expected=400)    
        self.assertEqual(res_dict['details'][0], 'Cannot delete element of versioned procedure')

        # check version 2
        version_dict_2 = self.get_procedure_version(procedure_id, 2)
        self.assertEqual(version_dict_2['version'], 2)

        structure_version_2 = self.get_version_structure(procedure_id, 2)
        logger.debug('structure_version_2: %s', json.dumps(structure_version_2, indent=4))
        self.assertEqual(structure_version_2['children'][0]['children'][0]['description'], 'Step 1-1')
        self.assertEqual(structure_version_2['children'][0]['children'][0]['number'], '1-1')
        self.assertEqual(structure_version_2['children'][0]['children'][1]['description'], 'Paragraph A')

        # update verion meta data
        version_description_new = 'new version description'
        version = 1
        self.update_procedure_version(procedure_id, version, {'version_description': version_description_new})
        version_dict = self.get_procedure_version(procedure_id, version)
        self.assertEqual(version_dict['version_description'], version_description_new)
        self.assertEqual(version_dict['time_released'], '')


        # release
        procedure_dict = self.get_procedure(procedure_id)
        self.assertEqual(procedure_dict['current_version'], 2)
        self.assertEqual(procedure_dict['current_released_version'], 0)

        version = 1
        institutional_release_id = 'A'
        self.update_procedure_version(procedure_id, version, {'institutional_release_id': institutional_release_id})
        self.update_procedure_version_status(procedure_id, version, {'action': 'RELEASE'})
        version_dict = self.get_procedure_version(procedure_id, version)
        self.assertTrue(len(version_dict['time_released']) > 0)
        self.assertEqual(version_dict['institutional_release_id'], institutional_release_id)

        version = 2
        institutional_release_id = 'B'
        self.update_procedure_version(procedure_id, version, {'institutional_release_id': institutional_release_id})
        self.update_procedure_version_status(procedure_id, version, {'action': 'RELEASE'})
        version_dict = self.get_procedure_version(procedure_id, version)
        self.assertTrue(len(version_dict['time_released']) > 0)
        self.assertEqual(version_dict['institutional_release_id'], institutional_release_id)

        procedure_dict = self.get_procedure(procedure_id)
        self.assertEqual(procedure_dict['current_version'], 2)
        self.assertEqual(procedure_dict['current_released_version'], 2)

        # unrelease
        self.update_procedure_version_status(procedure_id, version, {'action': 'UNRELEASE'})
        version_dict = self.get_procedure_version(procedure_id, version)
        self.assertEqual(version_dict['institutional_release_id'], 'B')
        self.assertEqual(version_dict['time_released'], '')

        procedure_dict = self.get_procedure(procedure_id)
        self.assertEqual(procedure_dict['current_version'], 2)
        self.assertEqual(procedure_dict['current_released_version'], 1)

    def test_procedure_tags(self):
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='CHILD',
            description='Paragraph A')         

        paragraph_a = res['elem']
        paragraph_a_id = paragraph_a['elem_id']
        
        # add paragraph
        res = self.add_paragraph(base_url=procedure_url,
            insert_after_id=paragraph_a_id,
            level='SIBLING',
            description='Paragraph B')   
        paragraph_b = res['elem']
        paragraph_b_id = paragraph_b['elem_id']        
        
        # add paragraph
        res = self.add_paragraph(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='SIBLING',
            description='Paragraph C')   
        paragraph_c = res['elem']
        paragraph_c_id = paragraph_c['elem_id']                
            
        ### Tags            
        tag1 = {
            'name': 'Tag 1',
            'description': 'First Tag'
        }
        tag2 = {
            'name': 'Tag 2',
            'description': 'Second Tag'
        }        
        tag3 = {
            'name': 'Tag 3',
            'description': 'Third Tag'
        }        
        
        res_dict = self.procedure_create_tag(procedure_id, tag1)
        logger.debug('procedure_create_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['name'], tag1['name'])
        self.assertEqual(res_dict[0]['description'], tag1['description'])
        self.assertTrue(len(res_dict[0]['tag_id']) > 0)
        tag_id_1 = res_dict[0]['tag_id']
        
        res_dict = self.procedure_create_tag(procedure_id, tag2)
        logger.debug('procedure_create_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(res_dict[0]['name'], tag1['name'])
        self.assertEqual(res_dict[0]['description'], tag1['description'])
        self.assertTrue(len(res_dict[0]['tag_id']) > 0)
        self.assertEqual(res_dict[1]['name'], tag2['name'])
        self.assertEqual(res_dict[1]['description'], tag2['description'])
        self.assertTrue(len(res_dict[1]['tag_id']) > 0)
        self.assertEqual(res_dict[0]['tag_id'], tag_id_1)
        tag_id_2 = res_dict[1]['tag_id']
        
        res_dict = self.procedure_create_tag(procedure_id, tag3)
        logger.debug('procedure_create_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(res_dict[0]['name'], tag1['name'])
        self.assertEqual(res_dict[0]['description'], tag1['description'])
        self.assertTrue(len(res_dict[0]['tag_id']) > 0)
        self.assertEqual(res_dict[1]['name'], tag2['name'])
        self.assertEqual(res_dict[1]['description'], tag2['description'])
        self.assertTrue(len(res_dict[1]['tag_id']) > 0)            
        self.assertEqual(res_dict[2]['name'], tag3['name'])
        self.assertEqual(res_dict[2]['description'], tag3['description'])
        self.assertTrue(len(res_dict[2]['tag_id']) > 0)
        tag_id_3 = res_dict[2]['tag_id']
        
        tag2b = {
            'name': 'Tag 2 B',
            'description': 'Updated description'            
        }
        res_dict = self.procedure_update_tag(procedure_id, tag_id_2, tag2b)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(res_dict[0]['name'], tag1['name'])
        self.assertEqual(res_dict[0]['description'], tag1['description'])
        self.assertTrue(len(res_dict[0]['tag_id']) > 0)
        self.assertEqual(res_dict[1]['name'], tag2b['name'])
        self.assertEqual(res_dict[1]['description'], tag2b['description'])
        self.assertTrue(len(res_dict[1]['tag_id']) > 0)            
        self.assertEqual(res_dict[2]['name'], tag3['name'])
        self.assertEqual(res_dict[2]['description'], tag3['description'])
        self.assertTrue(len(res_dict[2]['tag_id']) > 0)
        
        res_dict = self.procedure_delete_tag(procedure_id, tag_id_2)
        logger.debug('procedure_delete_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['tags']), 2)
        self.assertEqual(len(res_dict['elems']), 0)
        self.assertEqual(res_dict['tags'][0]['name'], tag1['name'])
        self.assertEqual(res_dict['tags'][0]['description'], tag1['description'])
        self.assertEqual(res_dict['tags'][0]['tag_id'], tag_id_1)     
        self.assertEqual(res_dict['tags'][1]['name'], tag3['name'])
        self.assertEqual(res_dict['tags'][1]['description'], tag3['description'])
        self.assertEqual(res_dict['tags'][1]['tag_id'], tag_id_3)

        # tagging and untagging elements
        res_dict = self.procedure_element_apply_tag(procedure_id, paragraph_a_id, tag_id_1)
        logger.debug('procedure_element_apply_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict[0]['tag_ids']), 1)
        self.assertEqual(res_dict[0]['tag_ids'][0], tag_id_1)
        
        res_dict = self.procedure_element_remove_tag(procedure_id, paragraph_a_id, tag_id_1)
        logger.debug('procedure_element_remove_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 1)   
        self.assertEqual(res_dict[0]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict[0]['tag_ids']), 0)
        
        res_dict = self.procedure_element_apply_tag(procedure_id, section_1_id, tag_id_1)
        logger.debug('procedure_element_apply_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(res_dict[0]['elem_id'], section_1_id)
        self.assertEqual(len(res_dict[0]['tag_ids']), 1)
        self.assertEqual(res_dict[0]['tag_ids'][0], tag_id_1)
        self.assertEqual(res_dict[1]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict[1]['tag_ids']), 1)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_1)
        self.assertEqual(res_dict[2]['elem_id'], paragraph_b_id)
        self.assertEqual(len(res_dict[2]['tag_ids']), 1)
        self.assertEqual(res_dict[2]['tag_ids'][0], tag_id_1)        
        
        res_dict = self.procedure_element_apply_tag(procedure_id, section_1_id, tag_id_2, 400)
        
        res_dict = self.procedure_element_apply_tag(procedure_id, section_1_id, tag_id_3)
        logger.debug('procedure_element_apply_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(res_dict[0]['elem_id'], section_1_id)
        self.assertEqual(len(res_dict[0]['tag_ids']), 2)
        self.assertEqual(res_dict[0]['tag_ids'][0], tag_id_1)
        self.assertEqual(res_dict[0]['tag_ids'][1], tag_id_3)
        self.assertEqual(res_dict[1]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict[1]['tag_ids']), 2)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_1)
        self.assertEqual(res_dict[1]['tag_ids'][1], tag_id_3)   
        self.assertEqual(res_dict[2]['elem_id'], paragraph_b_id)
        self.assertEqual(len(res_dict[2]['tag_ids']), 2)
        self.assertEqual(res_dict[2]['tag_ids'][0], tag_id_1)
        self.assertEqual(res_dict[2]['tag_ids'][1], tag_id_3)           
        
        # applying a tag again should result in no change
        res_dict = self.procedure_element_apply_tag(procedure_id, section_1_id, tag_id_3)
        logger.debug('procedure_element_apply_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 0)
        
        res_dict = self.procedure_element_remove_tag(procedure_id, paragraph_a_id, tag_id_1)
        logger.debug('procedure_element_remove_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(res_dict[0]['elem_id'], section_1_id)
        self.assertEqual(len(res_dict[0]['tag_ids']), 1)
        self.assertEqual(res_dict[0]['tag_ids'][0], tag_id_3)
        self.assertEqual(res_dict[1]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict[1]['tag_ids']), 1)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_3)   
        
        res_dict = self.procedure_element_remove_tag(procedure_id, section_1_id, tag_id_3)
        logger.debug('procedure_element_remove_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(res_dict[0]['elem_id'], section_1_id)
        self.assertEqual(len(res_dict[0]['tag_ids']), 0)     
        self.assertEqual(res_dict[1]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict[1]['tag_ids']), 0)
        self.assertEqual(res_dict[2]['elem_id'], paragraph_b_id)
        self.assertEqual(len(res_dict[2]['tag_ids']), 1)
        self.assertEqual(res_dict[2]['tag_ids'][0], tag_id_1)           
        
        res_dict = self.procedure_element_apply_tag(procedure_id, section_1_id, tag_id_1)
        logger.debug('procedure_element_apply_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(res_dict[0]['elem_id'], section_1_id)
        self.assertEqual(len(res_dict[0]['tag_ids']), 1)
        self.assertEqual(res_dict[0]['tag_ids'][0], tag_id_1)   
        self.assertEqual(res_dict[1]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict[1]['tag_ids']), 1)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_1)    
        
        res_dict = self.procedure_element_apply_tag(procedure_id, section_1_id, tag_id_3)
        logger.debug('procedure_element_apply_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(res_dict[0]['elem_id'], section_1_id)
        self.assertEqual(len(res_dict[0]['tag_ids']), 2)
        self.assertEqual(res_dict[0]['tag_ids'][0], tag_id_1)
        self.assertEqual(res_dict[0]['tag_ids'][1], tag_id_3)
        self.assertEqual(res_dict[1]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict[1]['tag_ids']), 2)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_1)
        self.assertEqual(res_dict[1]['tag_ids'][1], tag_id_3)              
        self.assertEqual(res_dict[2]['elem_id'], paragraph_b_id)
        self.assertEqual(len(res_dict[2]['tag_ids']), 2)
        self.assertEqual(res_dict[2]['tag_ids'][0], tag_id_1)
        self.assertEqual(res_dict[2]['tag_ids'][1], tag_id_3)     
        
        res_dict = self.procedure_element_remove_tag(procedure_id, paragraph_a_id, tag_id_1)
        logger.debug('procedure_element_apply_tag res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(res_dict[0]['elem_id'], section_1_id)
        self.assertEqual(len(res_dict[0]['tag_ids']), 1)
        self.assertEqual(res_dict[0]['tag_ids'][0], tag_id_3)
        self.assertEqual(res_dict[1]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict[1]['tag_ids']), 1)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_3)               
        
        ### create a version
        version_dict = self.create_procedure_version(procedure_id, 'First version', 'hongmank')
        logger.debug('create_procedure_version version_dict: %s', json.dumps(version_dict, indent=4))
        self.assertEqual(len(version_dict['tags']), 2)
        self.assertNotEqual(version_dict['tags'][0]['tag_id'], tag_id_1)
        self.assertNotEqual(version_dict['tags'][1]['tag_id'], tag_id_3)
        
        tag_id_1_v1 = version_dict['tags'][0]['tag_id']
        tag_id_3_v1 = version_dict['tags'][1]['tag_id']
        
        res_dict = self.get_version_elements(procedure_id=procedure_id, version=1)
        logger.debug('elements: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 4)
        self.assertEqual(len(res_dict[0]['tag_ids']), 1)
        self.assertEqual(res_dict[0]['tag_ids'][0], tag_id_3_v1)
        self.assertEqual(len(res_dict[1]['tag_ids']), 1)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_3_v1)   
        self.assertEqual(len(res_dict[2]['tag_ids']), 2)
        self.assertEqual(res_dict[2]['tag_ids'][0], tag_id_1_v1)
        self.assertEqual(res_dict[2]['tag_ids'][1], tag_id_3_v1)
        self.assertEqual(len(res_dict[3]['tag_ids']), 0)  
        
        outline_elems = self.get_outline(procedure_url, 1)
        logger.debug('outline_elems: %s', json.dumps(outline_elems, indent=4))
        self.assertEqual(len(outline_elems), 4)
        self.assertEqual(len(outline_elems[0]['tag_ids']), 1)
        self.assertEqual(outline_elems[0]['selected'], False)
        self.assertEqual(outline_elems[0]['tag_ids'][0], tag_id_3_v1)
        self.assertEqual(len(outline_elems[1]['tag_ids']), 1)
        self.assertEqual(outline_elems[1]['tag_ids'][0], tag_id_3_v1)
        self.assertEqual(outline_elems[1]['selected'], False)
        self.assertEqual(len(outline_elems[2]['tag_ids']), 2)
        self.assertEqual(outline_elems[2]['tag_ids'][0], tag_id_1_v1)
        self.assertEqual(outline_elems[2]['tag_ids'][1], tag_id_3_v1)
        self.assertEqual(outline_elems[2]['selected'], False)
        self.assertEqual(len(outline_elems[3]['tag_ids']), 0)
        self.assertEqual(outline_elems[3]['selected'], True)      
        
        tag_ids = [tag_id_1_v1]
        outline_elems = self.get_outline(procedure_url, 1, tag_ids)
        logger.debug('outline_elems: %s', json.dumps(outline_elems, indent=4))
        self.assertEqual(len(outline_elems), 4)
        self.assertEqual(len(outline_elems[0]['tag_ids']), 1)
        self.assertEqual(outline_elems[0]['tag_ids'][0], tag_id_3_v1)
        self.assertEqual(outline_elems[0]['selected'], False)        
        self.assertEqual(len(outline_elems[1]['tag_ids']), 1)
        self.assertEqual(outline_elems[1]['tag_ids'][0], tag_id_3_v1)  
        self.assertEqual(outline_elems[1]['selected'], False)        
        self.assertEqual(len(outline_elems[2]['tag_ids']), 2)
        self.assertEqual(outline_elems[2]['tag_ids'][0], tag_id_1_v1)
        self.assertEqual(outline_elems[2]['tag_ids'][1], tag_id_3_v1)
        self.assertEqual(outline_elems[2]['selected'], False)
        self.assertEqual(len(outline_elems[3]['tag_ids']), 0)
        self.assertEqual(outline_elems[3]['selected'], True)     
        
        tag_ids = [tag_id_3_v1]
        outline_elems = self.get_outline(procedure_url, 1, tag_ids)
        logger.debug('outline_elems: %s', json.dumps(outline_elems, indent=4))
        self.assertEqual(len(outline_elems), 4)
        self.assertEqual(len(outline_elems[0]['tag_ids']), 1)
        self.assertEqual(outline_elems[0]['tag_ids'][0], tag_id_3_v1)
        self.assertEqual(outline_elems[0]['selected'], True)        
        self.assertEqual(len(outline_elems[1]['tag_ids']), 1)
        self.assertEqual(outline_elems[1]['tag_ids'][0], tag_id_3_v1)  
        self.assertEqual(outline_elems[1]['selected'], True)        
        self.assertEqual(len(outline_elems[2]['tag_ids']), 2)
        self.assertEqual(outline_elems[2]['tag_ids'][0], tag_id_1_v1)
        self.assertEqual(outline_elems[2]['tag_ids'][1], tag_id_3_v1)
        self.assertEqual(outline_elems[2]['selected'], False)
        self.assertEqual(len(outline_elems[3]['tag_ids']), 0)
        self.assertEqual(outline_elems[3]['selected'], True)               
        
        tag_ids = [tag_id_1_v1, tag_id_3_v1]
        outline_elems = self.get_outline(procedure_url, 1, tag_ids)
        logger.debug('outline_elems: %s', json.dumps(outline_elems, indent=4))
        self.assertEqual(len(outline_elems), 4)
        self.assertEqual(len(outline_elems[0]['tag_ids']), 1)
        self.assertEqual(outline_elems[0]['tag_ids'][0], tag_id_3_v1)
        self.assertEqual(outline_elems[0]['selected'], True)
        self.assertEqual(len(outline_elems[1]['tag_ids']), 1)
        self.assertEqual(outline_elems[1]['tag_ids'][0], tag_id_3_v1)  
        self.assertEqual(outline_elems[1]['selected'], True)
        self.assertEqual(len(outline_elems[2]['tag_ids']), 2)
        self.assertEqual(outline_elems[2]['tag_ids'][0], tag_id_1_v1)
        self.assertEqual(outline_elems[2]['tag_ids'][1], tag_id_3_v1)     
        self.assertEqual(outline_elems[2]['selected'], True)        
        self.assertEqual(len(outline_elems[3]['tag_ids']), 0)
        self.assertEqual(outline_elems[3]['selected'], True)       
        
        ## Tag/untag elements again
        res_dict = self.procedure_element_remove_tag(procedure_id, section_1_id, tag_id_1) 
        res_dict = self.procedure_element_remove_tag(procedure_id, section_1_id, tag_id_3) 
        res_dict = self.procedure_element_apply_tag(procedure_id, section_1_id, tag_id_1)
        res_dict = self.procedure_element_apply_tag(procedure_id, section_1_id, tag_id_3)
        res_dict = self.procedure_element_remove_tag(procedure_id, paragraph_b_id, tag_id_3)      
       
        version_dict = self.create_procedure_version(procedure_id, 'Second version', 'hongmank')
        logger.debug('create_procedure_version version_dict: %s', json.dumps(version_dict, indent=4))
        self.assertEqual(len(version_dict['tags']), 2)
        self.assertNotEqual(version_dict['tags'][0]['tag_id'], tag_id_1)
        self.assertNotEqual(version_dict['tags'][1]['tag_id'], tag_id_3) 
        
        tag_id_1_v2 = version_dict['tags'][0]['tag_id']
        tag_id_3_v2 = version_dict['tags'][1]['tag_id']        
        
        # Check outline      
        res_dict = self.get_version_elements(procedure_id=procedure_id, version=2)
        logger.debug('elements: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 4)
        self.assertEqual(len(res_dict[0]['tag_ids']), 1)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(len(res_dict[1]['tag_ids']), 2)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(res_dict[1]['tag_ids'][0], tag_id_1_v2)   
        self.assertEqual(len(res_dict[2]['tag_ids']), 1)
        self.assertEqual(res_dict[2]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(len(res_dict[3]['tag_ids']), 0)  
        
        outline_elems = self.get_outline(procedure_url, 2)
        logger.debug('outline_elems: %s', json.dumps(outline_elems, indent=4))
        self.assertEqual(len(outline_elems), 4)
        self.assertEqual(len(outline_elems[0]['tag_ids']), 1)
        self.assertEqual(outline_elems[0]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(outline_elems[0]['selected'], False)
        self.assertEqual(len(outline_elems[1]['tag_ids']), 2)
        self.assertEqual(outline_elems[1]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(outline_elems[1]['tag_ids'][1], tag_id_3_v2)
        self.assertEqual(outline_elems[1]['selected'], False)
        self.assertEqual(len(outline_elems[2]['tag_ids']), 1)
        self.assertEqual(outline_elems[2]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(outline_elems[2]['selected'], False)
        self.assertEqual(len(outline_elems[3]['tag_ids']), 0)
        self.assertEqual(outline_elems[3]['selected'], True)      
        
        tag_ids = [tag_id_1_v2]
        outline_elems = self.get_outline(procedure_url, 2, tag_ids)
        logger.debug('outline_elems: %s', json.dumps(outline_elems, indent=4))
        self.assertEqual(len(outline_elems), 4)
        self.assertEqual(len(outline_elems[0]['tag_ids']), 1)
        self.assertEqual(outline_elems[0]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(outline_elems[0]['selected'], True)
        self.assertEqual(len(outline_elems[1]['tag_ids']), 2)
        self.assertEqual(outline_elems[1]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(outline_elems[1]['tag_ids'][1], tag_id_3_v2)
        self.assertEqual(outline_elems[1]['selected'], False)
        self.assertEqual(len(outline_elems[2]['tag_ids']), 1)
        self.assertEqual(outline_elems[2]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(outline_elems[2]['selected'], True)
        self.assertEqual(len(outline_elems[3]['tag_ids']), 0)
        self.assertEqual(outline_elems[3]['selected'], True)         
        
        tag_ids = [tag_id_3_v2]
        outline_elems = self.get_outline(procedure_url, 2, tag_ids)
        logger.debug('outline_elems: %s', json.dumps(outline_elems, indent=4))
        self.assertEqual(len(outline_elems), 4)
        self.assertEqual(len(outline_elems[0]['tag_ids']), 1)
        self.assertEqual(outline_elems[0]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(outline_elems[0]['selected'], False)
        self.assertEqual(len(outline_elems[1]['tag_ids']), 2)
        self.assertEqual(outline_elems[1]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(outline_elems[1]['tag_ids'][1], tag_id_3_v2)
        self.assertEqual(outline_elems[1]['selected'], False)
        self.assertEqual(len(outline_elems[2]['tag_ids']), 1)
        self.assertEqual(outline_elems[2]['tag_ids'][0], tag_id_1_v2)
        self.assertEqual(outline_elems[2]['selected'], False)
        self.assertEqual(len(outline_elems[3]['tag_ids']), 0)
        self.assertEqual(outline_elems[3]['selected'], True)                
        
        ## remove tags from working version
        res_dict = self.procedure_delete_tag(procedure_id, tag_id_1)
        logger.debug('procedure_delete_tag res_dict: %s', json.dumps(res_dict, indent=4))        
        self.assertEqual(len(res_dict['tags']), 1)
        self.assertEqual(res_dict['tags'][0]['name'], tag3['name'])
        self.assertEqual(res_dict['tags'][0]['description'], tag3['description'])
        self.assertEqual(res_dict['tags'][0]['tag_id'], tag_id_3)     
        self.assertEqual(len(res_dict['elems']), 3)
        self.assertEqual(res_dict['elems'][0]['elem_id'], section_1_id)
        self.assertEqual(len(res_dict['elems'][0]['tag_ids']), 0)
        self.assertEqual(res_dict['elems'][1]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict['elems'][1]['tag_ids']), 1)
        self.assertEqual(res_dict['elems'][1]['tag_ids'][0], tag_id_3)
        self.assertEqual(res_dict['elems'][2]['elem_id'], paragraph_b_id)
        self.assertEqual(len(res_dict['elems'][2]['tag_ids']), 0)        
        
        res_dict = self.procedure_delete_tag(procedure_id, tag_id_3)
        logger.debug('procedure_delete_tag res_dict: %s', json.dumps(res_dict, indent=4))        
        self.assertEqual(len(res_dict['tags']), 0)   
        self.assertEqual(len(res_dict['elems']), 1)
        self.assertEqual(res_dict['elems'][0]['elem_id'], paragraph_a_id)
        self.assertEqual(len(res_dict['elems'][0]['tag_ids']), 0)

        
    def test_comments(self):
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')
        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1 source')

        section_1 = res['elem']
        section_id_1 = section_1['elem_id']
        logger.debug('working copy section_id_1: %s', section_id_1)
        
        # cannot add comment to a working copy
        procedure_version_url = shared_dict['host'] + '/procedures/' + procedure_id + '/versions/0'
        res_dict = self.add_conversation(procedure_version_url, section_id_1, {'type': 'COMMENT'}, code_expected=400)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))

        # add version
        version_dict = self.create_procedure_version(procedure_id, 'First version', 'hongmank')
        self.assertEqual(version_dict['version'], 1)
        
        procedure_version_url = shared_dict['host'] + '/procedures/' + procedure_id + '/versions/1'
        logger.debug('procedure_version_url: %s', procedure_version_url)
                
        res_dict = self.get_version_elements(procedure_id=procedure_id, version=1)
        logger.debug('elements: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 1)
        section_id_1 = res_dict[0]['elem_id']
        logger.debug('version 1 section_id_1: %s', section_id_1)

        # only generic comment is allowed for procedure
        res_dict = self.add_conversation(procedure_version_url, section_id_1, {'type': 'DATA_REVIEW_COMMENT'}, code_expected=400)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))

        # check conversations count
        version_dict = self.get_procedure_version(procedure_id, 1)
        self.assertEqual(version_dict['conversations_count'], 0)
        self.assertEqual(version_dict['unresolved_conversations_count'], 0)
        
        # Add comment to section                
        content1 = 'This is the first comment for the section'
        res_dict = self.add_conversation(procedure_version_url, section_id_1, {'type': 'COMMENT'})
        conversation_id_1 = res_dict['conversation_id']
        # should have an empty comment
        self.assertEqual(len(res_dict['comments']), 1)
        comment_1 = res_dict['comments'][0]
        comment_id_1 = comment_1['comment_id']
        time_updated_1 = comment_1['time_updated']
        self.assertEqual(comment_1['content'], '')
        self.assertEqual('type' in comment_1, False)
        self.assertTrue(len(comment_1['user_name']) > 0)

        # check conversations count
        version_dict = self.get_procedure_version(procedure_id, 1)
        self.assertEqual(version_dict['conversations_count'], 1)
        self.assertEqual(version_dict['unresolved_conversations_count'], 1)     
        
        res_dict = self.get_version_elements(procedure_id=procedure_id, version=1)
        logger.debug('elements: %s', json.dumps(res_dict, indent=4))
        
        res_dict = self.update_comment(procedure_version_url, section_id_1, conversation_id_1, comment_id_1, content1)
        self.assertEqual(res_dict['content'], content1)
        
        res_dict = self.get_version_elements(procedure_id=procedure_id, version=1)
        logger.debug('elements: %s', json.dumps(res_dict, indent=4))

        time.sleep(0.01)

        # update comment
        content1b = 'This is the first comment for the section and updated'

        res_dict = self.update_comment(procedure_version_url, section_id_1, conversation_id_1, comment_id_1, content1b)

        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['content'], content1b)        
        time_updated_1b = res_dict['time_updated']      
        self.assertGreater(time_updated_1b, time_updated_1)   
        self.assertTrue(len(res_dict['user_name']) > 0)        

        # set it back
        res_dict = self.update_comment(procedure_version_url, section_id_1, conversation_id_1, comment_id_1, content1)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['content'], content1)                   

        # check the section
        res_dict = self.get_version_elements(procedure_id=procedure_id, version=1)
        section_dict = res_dict[0]
        logger.debug('section_dict: %s', json.dumps(section_dict, indent=4))
        self.assertEqual(len(section_dict['conversations']), 1)
        self.assertEqual(len(section_dict['conversations'][0]['comments']), 1)
        
        self.assertEqual(section_dict['conversations'][0]['comments'][0]['content'], content1)

        # Add another comment to section
        content2 = 'This is the second comment for the section'
        res_dict = self.add_comment(procedure_version_url, section_id_1, conversation_id_1, content2)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        comment_id_2 = res_dict['comment_id']
        self.assertEqual(res_dict['content'], content2)

        # check the section
        res_dict = self.get_version_elements(procedure_id=procedure_id, version=1)
        section_dict = res_dict[0]
        logger.debug('section_dict: %s', json.dumps(section_dict, indent=4))
        self.assertEqual(len(section_dict['conversations']), 1)
        self.assertEqual(len(section_dict['conversations'][0]['comments']), 2)        
        self.assertEqual(section_dict['conversations'][0]['comments'][0]['content'], content1)
        self.assertEqual(section_dict['conversations'][0]['comments'][1]['content'], content2)

        # get comments
        comments_dict = self.get_comments(procedure_version_url, section_id_1, conversation_id_1)
        logger.debug('comments_dict: %s', json.dumps(comments_dict, indent=4))
        self.assertEqual(len(comments_dict), 2)
        self.assertEqual(comments_dict[0]['content'], content1)
        self.assertEqual(comments_dict[1]['content'], content2)

        # get comment
        comment1_dict = self.get_comment(procedure_version_url, section_id_1, conversation_id_1, comment_id_1)
        logger.debug('comment1_dict: %s', json.dumps(comment1_dict, indent=4))
        self.assertEqual(comment1_dict['content'], content1)

        # get comment
        comment2_dict = self.get_comment(procedure_version_url, section_id_1, conversation_id_1, comment_id_2)
        logger.debug('comment2_dict: %s', json.dumps(comment2_dict, indent=4))
        self.assertEqual(comment2_dict['content'], content2)

        # delete comment
        self.delete_comment(procedure_version_url, section_id_1, conversation_id_1, comment_id_1)

        # delete a non-existing comment
        self.delete_comment(procedure_version_url, 'not_an_elem_id', conversation_id_1, 'not_a_comment_id', 400)

        # delete a non-existing comment
        self.delete_comment(procedure_version_url, section_id_1, conversation_id_1, 'not_a_comment_id', 400)

        # get comments
        comments_dict = self.get_comments(procedure_version_url, section_id_1, conversation_id_1)
        logger.debug('comments_dict: %s', json.dumps(comments_dict, indent=4))
        self.assertEqual(len(comments_dict), 1)
        self.assertEqual(comments_dict[0]['content'], content2)

        # check conversations count
        version_dict = self.get_procedure_version(procedure_id, 1)
        self.assertEqual(version_dict['conversations_count'], 1)
        self.assertEqual(version_dict['unresolved_conversations_count'], 1)
        
        # add another conversation
        content_2_1 = 'This is the first comment of the second conversation'
        res_dict = self.add_conversation(procedure_version_url, section_id_1, {'type': 'COMMENT'})
        conversation_id_2 = res_dict['conversation_id']
        comment_2_1 = res_dict['comments'][0]
        comment_id_2_1 = comment_2_1['comment_id']        

        # check conversations count
        version_dict = self.get_procedure_version(procedure_id, 1)
        self.assertEqual(version_dict['conversations_count'], 2)
        self.assertEqual(version_dict['unresolved_conversations_count'], 2)
         
        res_dict = self.update_comment(procedure_version_url, section_id_1, conversation_id_2, comment_id_2_1, content_2_1)
        self.assertEqual(res_dict['content'], content_2_1)         
        
        # add another comment
        content_2_2 = 'This is the second comment of the second conversation'
        res_dict = self.add_comment(procedure_version_url, section_id_1, conversation_id_2, content_2_2)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        comment_id_2_2 = res_dict['comment_id']
        self.assertEqual(res_dict['content'], content_2_2)
        
        # get conversations
        res_dict = self.get_conversations(procedure_version_url, section_id_1)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(len(res_dict[1]['comments']), 2)
        self.assertEqual(res_dict[1]['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict[1]['comments'][1]['content'], content_2_2)
        
        # get conversation
        res_dict = self.get_conversation(procedure_version_url, section_id_1, conversation_id_2)
        self.assertEqual(len(res_dict['comments']), 2)
        self.assertEqual(res_dict['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict['comments'][1]['content'], content_2_2)     
        self.assertEqual(res_dict['status'], 'UNRESOLVED') 
        self.assertEqual(res_dict['time_resolved'], '')
        self.assertEqual(res_dict['resolved_by'], '')
        
        # resolve conversation
        res_dict = self.update_conversation(procedure_version_url, section_id_1, conversation_id_2, {'status': 'RESOLVED'})
        # check conversation
        res_dict = self.get_conversation(procedure_version_url, section_id_1, conversation_id_2)
        self.assertEqual(len(res_dict['comments']), 2)
        self.assertEqual(res_dict['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict['comments'][1]['content'], content_2_2)     
        self.assertEqual(res_dict['status'], 'RESOLVED') 
        self.assertTrue(len(res_dict['time_resolved']) > 0)
        self.assertTrue(len(res_dict['resolved_by']) > 0) 

        # check conversations count
        version_dict = self.get_procedure_version(procedure_id, 1)
        self.assertEqual(version_dict['conversations_count'], 2)
        self.assertEqual(version_dict['unresolved_conversations_count'], 1)
        
        # unresolve conversation
        res_dict = self.update_conversation(procedure_version_url, section_id_1, conversation_id_2, {'status': 'UNRESOLVED'})
        # check conversation
        res_dict = self.get_conversation(procedure_version_url, section_id_1, conversation_id_2)
        self.assertEqual(len(res_dict['comments']), 2)
        self.assertEqual(res_dict['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict['comments'][1]['content'], content_2_2)     
        self.assertEqual(res_dict['status'], 'UNRESOLVED') 
        self.assertEqual(res_dict['time_resolved'], '')
        self.assertEqual(res_dict['resolved_by'], '')

        # check conversations count
        version_dict = self.get_procedure_version(procedure_id, 1)
        self.assertEqual(version_dict['conversations_count'], 2)
        self.assertEqual(version_dict['unresolved_conversations_count'], 2)
        
        # delete conversation
        res_dict = self.delete_conversation(procedure_version_url, section_id_1, conversation_id_1)
        
        # check conversations
        res_dict = self.get_conversations(procedure_version_url, section_id_1)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(len(res_dict[0]['comments']), 2)
        self.assertEqual(res_dict[0]['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict[0]['comments'][1]['content'], content_2_2)

        # check conversations count
        version_dict = self.get_procedure_version(procedure_id, 1)
        self.assertEqual(version_dict['conversations_count'], 1)
        self.assertEqual(version_dict['unresolved_conversations_count'], 1)
        
    def test_comments_filter(self):
        
        id_dict = self.create_procedure_example()
        procedure_url = id_dict['procedure_url']         
        procedure_id = id_dict['procedure_id']
        
        version_dict = self.create_procedure_version(procedure_id, 'First version', '')
        
        procedure_version_url = shared_dict['host'] + '/procedures/' + procedure_id + '/versions/' + str(version_dict['version'])
        logger.debug('procedure_version_url: %s', procedure_version_url)        
        
        elements = self.get_version_elements(procedure_id=procedure_id, version=1)
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 6)
        
        section_id_1 = elements[0]['elem_id']
        section_id_1_1 = elements[1]['elem_id']
        section_id_1_2 = elements[2]['elem_id']
        section_id_2 = elements[3]['elem_id']
        section_id_2_1 = elements[4]['elem_id']
        section_id_2_2 = elements[5]['elem_id']   
        
        res_dict = self.add_conversation(procedure_version_url, section_id_1_1, {'type': 'COMMENT'})
        res_dict = self.add_conversation(procedure_version_url, section_id_2, {'type': 'COMMENT'})
        res_dict = self.add_conversation(procedure_version_url, section_id_2_1, {'type': 'COMMENT'})
        
        elements = self.get_version_elements(procedure_id=procedure_id, version=1, params={'comment_filter': 'ON'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0]['elem_id'], section_id_1_1)
        self.assertEqual(elements[1]['elem_id'], section_id_2)
        self.assertEqual(elements[2]['elem_id'], section_id_2_1)     
        
        elements = self.get_version_elements(procedure_id=procedure_id, version=1, params={'comment_filter': 'OFF'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 6)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], section_id_1_1)
        self.assertEqual(elements[2]['elem_id'], section_id_1_2)    
        self.assertEqual(elements[3]['elem_id'], section_id_2)
        self.assertEqual(elements[4]['elem_id'], section_id_2_1)
        self.assertEqual(elements[5]['elem_id'], section_id_2_2)              
        
        elements = self.get_version_elements(procedure_id=procedure_id, version=1, params={'comment_filter': 'ON', 'limit': 2})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], section_id_1_1)
        self.assertEqual(elements[1]['elem_id'], section_id_2)          
        
        elements = self.get_version_elements(procedure_id=procedure_id, version=1, params={'comment_filter': 'ON', 'offset': 1, 'limit': 2})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], section_id_2)
        self.assertEqual(elements[1]['elem_id'], section_id_2_1)    
        
        elements = self.get_version_elements(procedure_id=procedure_id, version=1, params={'all_elements': 'ON', 'comment_filter': 'OFF'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 6)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], section_id_1_1)
        self.assertEqual(elements[2]['elem_id'], section_id_1_2)    
        self.assertEqual(elements[3]['elem_id'], section_id_2)
        self.assertEqual(elements[4]['elem_id'], section_id_2_1)
        self.assertEqual(elements[5]['elem_id'], section_id_2_2)   
        
        elements = self.get_version_elements(procedure_id=procedure_id, version=1, params={'all_elements': 'ON', 'comment_filter': 'ON'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 6)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], section_id_1_1)
        self.assertEqual(elements[2]['elem_id'], section_id_1_2)    
        self.assertEqual(elements[3]['elem_id'], section_id_2)
        self.assertEqual(elements[4]['elem_id'], section_id_2_1)
        self.assertEqual(elements[5]['elem_id'], section_id_2_2)            
        
        elements = self.get_version_elements(procedure_id=procedure_id, version=1, params={'all_elements': 'ON', 'comment_filter': 'ON', 'limit': 2})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], section_id_1_1)
        
        elements = self.get_version_elements(procedure_id=procedure_id, version=1, params={'all_elements': 'ON', 'comment_filter': 'ON', 'offset': 1, 'limit': 2})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], section_id_1_1)
        self.assertEqual(elements[1]['elem_id'], section_id_1_2)            
                
    def test_files(self):

        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')
        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        # add step
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Step 1-1',
            description='Step 1-1')

        step_1_1 = res['elem']
        step_1_1_id = step_1_1['elem_id']

        # Add File to procedure
        fileUrl1 = "location/path/to/file"
        fileUrl2 = "location/path/to/file2"

        print('shared dict host 2:', shared_dict['host'])

        res_dict = self.add_procedure_file_meta(procedure_id, fileUrl1)
        procedure_file_id_1 = res_dict['file_id']

        res_dict = self.add_procedure_file_meta(procedure_id, fileUrl2)
        procedure_file_id_2 = res_dict['file_id']

        #Get File from comment
        res_dict = self.get_procedure_file(procedure_id, procedure_file_id_1)
        self.assertEqual(res_dict['url'], fileUrl1)

        #Get files from comments
        url = '{0}/procedures/{1}/files'.format(shared_dict['host'], procedure_id)
        logger.debug('GET: %s', url)
        result = requests.get(url,
            headers=shared_dict['headers'])
        res_dict = json.loads(result.text)
        self.assertEqual(int(result.headers['x-total-count']), 2)
        self.assertEqual(res_dict[1]['url'], fileUrl2)

        result = requests.get(url,
            headers=shared_dict['headers'],
            params={"offset":1, 'limit' : 1})
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)

        #delete commment file
        self.delete_procedure_file(procedure_id, procedure_file_id_1)
        logger.debug('GET: %s', url)
        result = requests.get(url,
            headers=shared_dict['headers'])
        res_dict = json.loads(result.text)
        self.assertEqual(int(result.headers['x-total-count']), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)

        # Add File to element
        res_dict = self.add_elem_file_meta(procedure_url, section_1_id, fileUrl1)
        elem_file_id_1 = res_dict['file_id']

        res_dict = self.add_elem_file_meta(procedure_url, section_1_id, fileUrl2)
        elem_file_id_2 = res_dict['file_id']

        #Get File from element
        res_dict = self.get_elem_file(procedure_url, section_1_id, elem_file_id_1)
        self.assertEqual(res_dict['url'], fileUrl1)

        #Get files from elements
        url = '{0}/procedures/{1}/elements/{2}/files'.format(shared_dict['host'], procedure_id, section_1_id)
        logger.debug('GET: %s', url)
        result = requests.get(url,
            headers=shared_dict['headers'])
        res_dict = json.loads(result.text)
        self.assertEqual(int(result.headers['x-total-count']), 2)
        self.assertEqual(res_dict[1]['url'], fileUrl2)

        logger.debug('GET: %s', url)
        result = requests.get(url,
            headers=shared_dict['headers'],
            params={"offset":1, 'limit' : 1})
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)

        #delete element file
        self.delete_elem_file(procedure_url, section_1_id, elem_file_id_1)
        logger.debug('GET: %s', url)
        result = requests.get(url,
            headers=shared_dict['headers'])
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)
        
        ### test files attached to element comment
        version_dict = self.create_procedure_version(procedure_id, 'First version', '')
        procedure_version_url = shared_dict['host'] + '/procedures/' + procedure_id + '/versions/1'
        
        res_dict = self.get_version_elements(procedure_id=procedure_id, version=1)
        logger.debug('elements: %s', json.dumps(res_dict, indent=4))

        section_id_1 = res_dict[0]['elem_id']
        logger.debug('version 1 section_id_1: %s', section_id_1)        
        res_dict = self.add_conversation(procedure_version_url, section_id_1, {'type': 'COMMENT'})
        conversation_id = res_dict['conversation_id']
        comment_1 = res_dict['comments'][0]
        comment_id_1 = comment_1['comment_id']
        
        content1 = 'This is the first comment for the section'
        res_dict = self.update_comment(procedure_version_url, section_id_1, conversation_id, comment_id_1, content1)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['content'], content1)           
        
        # Add File to comment
        fileUrl1 = "location/path/to/file"
        res_dict = self.add_comment_file_meta(procedure_version_url, section_id_1, conversation_id, comment_id_1, fileUrl1)
        comment_file_id_1 = res_dict['file_id']

        fileUrl2 = "location/path/to/file2"
        res_dict = self.add_comment_file_meta(procedure_version_url, section_id_1, conversation_id, comment_id_1, fileUrl2)
        comment_file_id_2 = res_dict['file_id']

        #Get File from comment
        res_dict = self.get_comment_file(procedure_version_url, section_id_1, conversation_id, comment_id_1, comment_file_id_1)
        self.assertEqual(res_dict['url'], fileUrl1)

        #Get files from comment
        res_dict = self.get_comment_files(procedure_version_url, section_id_1, conversation_id, comment_id_1)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(res_dict[0]['url'], fileUrl1)
        self.assertEqual(res_dict[1]['url'], fileUrl2)

        res_dict = self.get_comment_files(procedure_version_url, section_id_1, conversation_id, comment_id_1, offset=1, limit=1)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)

        #delete commment file
        self.delete_comment_file(procedure_version_url, section_id_1, conversation_id, comment_id_1, comment_file_id_1)
        
        res_dict = self.get_comment_files(procedure_version_url, section_id_1, conversation_id, comment_id_1)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)        
          

    def test_procedure_load(self):

        ## create source procedure
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id_source = procedure_dict['procedure_id']
        procedure_url_source = shared_dict['host'] + '/procedures/' + procedure_id_source

        # Add section
        res = self.add_section(base_url=procedure_url_source,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1 source')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url_source,
            insert_after_id=section_1_id,
            level='CHILD',
            description='Paragraph A Source')

        paragraph_a = res['elem']
        paragraph_a_id = paragraph_a['elem_id']

        # add step

        res = self.add_step_generic(base_url=procedure_url_source,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Step 1-1 Source',
            description='Step 1-1 Source')

        step_1_1 = res['elem']
        step_1_1_id = step_1_1['elem_id']
        
        # add tags
        tag1 = {
            'name': 'Tag 1',
            'description': 'First Tag'
        }
        tag2 = {
            'name': 'Tag 2',
            'description': 'Second Tag'
        }        
        tag3 = {
            'name': 'Tag 3',
            'description': 'Third Tag'
        }                   

        # For the source        
        res_dict = self.procedure_create_tag(procedure_id_source, tag1)
        res_dict = self.procedure_create_tag(procedure_id_source, tag2)
        tag_id_1 = res_dict[0]['tag_id']
        tag_id_2 = res_dict[1]['tag_id']
        
        res_dict = self.procedure_element_apply_tag(procedure_id_source, paragraph_a_id, tag_id_1)
        res_dict = self.procedure_element_apply_tag(procedure_id_source, paragraph_a_id, tag_id_2)        

        # add version
        version_dict = self.create_procedure_version(procedure_id_source, 'First version', 'hongmank')
        self.assertEqual(version_dict['version'], 1)
        
        structure_version_1 = self.get_version_structure(procedure_id_source, 1)
        self.assertEqual(structure_version_1['children'][0]['children'][1]['description'], 'Paragraph A Source')
        self.assertEqual(len(structure_version_1['children'][0]['children'][1]['tag_ids']), 2)
        self.assertNotEqual(structure_version_1['children'][0]['children'][1]['tag_ids'][0], tag_id_1)
        self.assertNotEqual(structure_version_1['children'][0]['children'][1]['tag_ids'][1], tag_id_2)
        
        tag_id_1_v1 = structure_version_1['children'][0]['children'][1]['tag_ids'][0]
        tag_id_2_v1 = structure_version_1['children'][0]['children'][1]['tag_ids'][1]

        ## create target procedure
        rand_2 = random_string()
        title_2 = 'title_' + rand_2
        procedure_dict = self.create_procedure(title_2, 'Test procedure', '', 'hongmank')

        procedure_id_target = procedure_dict['procedure_id']
        procedure_url_target = shared_dict['host'] + '/procedures/' + procedure_id_target

        # add tag         
        res_dict = self.procedure_create_tag(procedure_id_target, tag3)
        tag_id_3 = res_dict[0]['tag_id']     
        
        # Add section
        res = self.add_section(base_url=procedure_url_target,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1')
        section_1_target = res['elem']
        section_1_id_target = section_1_target['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url_target,
            insert_after_id=section_1_id_target,
            level='CHILD',
            description='Paragraph A')

        res = self.add_section(base_url=procedure_url_target,
            insert_after_id=section_1_id_target,
            level='SIBLING',
            description='Section 2')

        # reload
        self.load_procedure_version(procedure_id_target, procedure_id_source, 1)

        # check the working copy of target
        version_dict_0 = self.get_procedure_version(procedure_id_target, 0)
        self.assertEqual(version_dict_0['version'], 0)
        self.assertEqual(len(version_dict_0['tags']), 2)
        self.assertEqual(version_dict_0['tags'][0]['description'], tag1['description'])
        self.assertEqual(version_dict_0['tags'][1]['description'], tag2['description'])
        tag_id_1_imported = version_dict_0['tags'][0]['tag_id']
        tag_id_2_imported = version_dict_0['tags'][1]['tag_id']
        self.assertNotEqual(tag_id_1_v1, tag_id_1_imported)
        self.assertNotEqual(tag_id_2_v1, tag_id_2_imported)        

        structure_version_0 = self.get_version_structure(procedure_id_target, 0)
        logger.debug('structure_version_0: %s', json.dumps(structure_version_0, indent=4))
        self.assertEqual(structure_version_0['children'][0]['children'][0]['description'], 'Step 1-1 Source')
        self.assertEqual(structure_version_0['children'][0]['children'][0]['number'], '1-1')

        self.assertEqual(structure_version_0['children'][0]['children'][1]['description'], 'Paragraph A Source')
        self.assertEqual(len(structure_version_0['children'][0]['children'][1]['tag_ids']), 2)
        self.assertEqual(structure_version_0['children'][0]['children'][1]['tag_ids'][0], tag_id_1_imported)
        self.assertEqual(structure_version_0['children'][0]['children'][1]['tag_ids'][1], tag_id_2_imported)        

    def test_procedure_version_import(self):

        ## create source procedure
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id_source = procedure_dict['procedure_id']
        procedure_url_source = shared_dict['host'] + '/procedures/' + procedure_id_source

        # Add section
        res = self.add_section(base_url=procedure_url_source,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1 source')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url_source,
            insert_after_id=section_1_id,
            level='CHILD',
            description='Paragraph A Source')

        paragraph_a = res['elem']
        paragraph_a_id = paragraph_a['elem_id']

        # add step

        res = self.add_step_generic(base_url=procedure_url_source,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Step 1-1 Source',
            description='Step 1-1 Source')

        step_1_1 = res['elem']
        step_1_1_id = step_1_1['elem_id']

        # add tags
        tag1 = {
            'name': 'Tag 1',
            'description': 'First Tag'
        }
        tag2 = {
            'name': 'Tag 2',
            'description': 'Second Tag'
        }        
        tag3 = {
            'name': 'Tag 3',
            'description': 'Third Tag'
        }                   

        # For the source        
        res_dict = self.procedure_create_tag(procedure_id_source, tag1)
        res_dict = self.procedure_create_tag(procedure_id_source, tag2)
        tag_id_1 = res_dict[0]['tag_id']
        tag_id_2 = res_dict[1]['tag_id']
        
        res_dict = self.procedure_element_apply_tag(procedure_id_source, paragraph_a_id, tag_id_1)
        res_dict = self.procedure_element_apply_tag(procedure_id_source, paragraph_a_id, tag_id_2)        

        # add version
        version_dict = self.create_procedure_version(procedure_id_source, 'First version', 'hongmank')
        self.assertEqual(version_dict['version'], 1)
        
        structure_version_1 = self.get_version_structure(procedure_id_source, 1)
        self.assertEqual(structure_version_1['children'][0]['children'][1]['description'], 'Paragraph A Source')
        self.assertEqual(len(structure_version_1['children'][0]['children'][1]['tag_ids']), 2)
        self.assertNotEqual(structure_version_1['children'][0]['children'][1]['tag_ids'][0], tag_id_1)
        self.assertNotEqual(structure_version_1['children'][0]['children'][1]['tag_ids'][1], tag_id_2)
        
        tag_id_1_v1 = structure_version_1['children'][0]['children'][1]['tag_ids'][0]
        tag_id_2_v1 = structure_version_1['children'][0]['children'][1]['tag_ids'][1]
        
        ## create target procedure
        rand_2 = random_string()
        title_2 = 'title_' + rand_2
        procedure_dict = self.create_procedure(title_2, 'Test procedure', '', 'hongmank')

        procedure_id_target = procedure_dict['procedure_id']
        procedure_url_target = shared_dict['host'] + '/procedures/' + procedure_id_target
        
        # add tag         
        res_dict = self.procedure_create_tag(procedure_id_target, tag3)
        tag_id_3 = res_dict[0]['tag_id']             

        # Add section
        res = self.add_section(base_url=procedure_url_target,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1')
        section_1_target = res['elem']
        section_1_id_target = section_1_target['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url_target,
            insert_after_id=section_1_id_target,
            level='CHILD',
            description='Paragraph A')

        res = self.add_section(base_url=procedure_url_target,
            insert_after_id=section_1_id_target,
            level='SIBLING',
            description='Section 2')

        # get source procedure version
        version_structure = self.get_version_structure(procedure_id_source, 1)

        # import into target procedure
        logger.debug('version_structure: %s', json.dumps(version_structure, indent=4))
        self.import_procedure_version(procedure_id_target, version_structure)

        # check the working copy of target
        logger.debug('procedure_url_target=%s', procedure_url_target)
        version_dict_0 = self.get_procedure_version(procedure_id_target, 0)
        self.assertEqual(version_dict_0['version'], 0)
        self.assertEqual(len(version_dict_0['tags']), 2)
        self.assertEqual(version_dict_0['tags'][0]['description'], tag1['description'])
        self.assertEqual(version_dict_0['tags'][1]['description'], tag2['description'])
        tag_id_1_imported = version_dict_0['tags'][0]['tag_id']
        tag_id_2_imported = version_dict_0['tags'][1]['tag_id']
        self.assertNotEqual(tag_id_1_v1, tag_id_1_imported)
        self.assertNotEqual(tag_id_2_v1, tag_id_2_imported)            

        structure_version_0 = self.get_version_structure(procedure_id_target, 0)
        logger.debug('structure_version_0: %s', json.dumps(structure_version_0, indent=4))
        self.assertEqual(structure_version_0['children'][0]['children'][0]['description'], 'Step 1-1 Source')
        self.assertEqual(structure_version_0['children'][0]['children'][0]['number'], '1-1')
        self.assertEqual(structure_version_0['children'][0]['children'][1]['description'], 'Paragraph A Source')
        self.assertEqual(len(structure_version_0['children'][0]['children'][1]['tag_ids']), 2)
        self.assertEqual(structure_version_0['children'][0]['children'][1]['tag_ids'][0], tag_id_1_imported)
        self.assertEqual(structure_version_0['children'][0]['children'][1]['tag_ids'][1], tag_id_2_imported)    

    def compare_procedure_info(self, procedure_info, procedure_info_predict):
        self.assertEqual(procedure_info['procedure_id'], procedure_info_predict['procedure_id'])
        self.assertEqual(procedure_info['title'], procedure_info_predict['title'])
        self.assertEqual(procedure_info['description'], procedure_info_predict['description']) 
        self.assertEqual(procedure_info['institutional_id'], procedure_info_predict['institutional_id']) 
        self.assertEqual(procedure_info['author'], procedure_info_predict['author'])
        
    def test_procedure_import(self):
        ## create procedure
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1 source')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        version_dict = self.create_procedure_version(procedure_id, 'First version', 'hongmank')
        self.assertEqual(version_dict['version'], 1)

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='CHILD',
            description='Paragraph A Source')

        paragraph_a = res['elem']
        paragraph_a_id = paragraph_a['elem_id']

        version_dict = self.create_procedure_version(procedure_id, 'Second version', 'hongmank')
        self.assertEqual(version_dict['version'], 2)

        # add step
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Step 1-1 Source',
            description='Step 1-1 Source')

        step_1_1 = res['elem']
        step_1_1_id = step_1_1['elem_id']

        # add tags
        tag1 = {
            'name': 'Tag 1',
            'description': 'First Tag'
        }
        tag2 = {
            'name': 'Tag 2',
            'description': 'Second Tag'
        }        
        tag3 = {
            'name': 'Tag 3',
            'description': 'Third Tag'
        }                   

        # For the source        
        res_dict = self.procedure_create_tag(procedure_id, tag1)
        res_dict = self.procedure_create_tag(procedure_id, tag2)
        tag_id_1 = res_dict[0]['tag_id']
        tag_id_2 = res_dict[1]['tag_id']
        
        res_dict = self.procedure_element_apply_tag(procedure_id, paragraph_a_id, tag_id_1)
        res_dict = self.procedure_element_apply_tag(procedure_id, paragraph_a_id, tag_id_2)        

        # add version
        version_dict = self.create_procedure_version(procedure_id, 'Third version', 'hongmank')
        self.assertEqual(version_dict['version'], 3)

        # release version 1
        data = {'action': 'SUBMIT'}
        res_dict = self.update_procedure_version_status(procedure_id, 1, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertEqual(res_dict['time_approved'], '')  
        self.assertEqual(res_dict['time_released'], '')  
        self.assertEqual(res_dict['institutional_release_id'], '')
        self.assertEqual(res_dict['status'], 'SUBMITTED')

        data = {'action': 'APPROVE'}
        res_dict = self.update_procedure_version_status(procedure_id, 1, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertTrue(len(res_dict['time_approved']) > 0)
        self.assertEqual(res_dict['time_released'], '')  
        self.assertEqual(res_dict['institutional_release_id'], '')
        self.assertEqual(res_dict['status'], 'APPROVED')

        res_dict = self.update_procedure_version(procedure_id, 1, {'institutional_release_id': 'Initial Release'})
        data = {'action': 'RELEASE'}
        res_dict = self.update_procedure_version_status(procedure_id, 1, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertTrue(len(res_dict['time_approved']) > 0)
        self.assertTrue(len(res_dict['time_released']) > 0)
        self.assertEqual(res_dict['institutional_release_id'], 'Initial Release')
        self.assertEqual(res_dict['status'], 'RELEASED')

        # release version 3
        data = {'action': 'SUBMIT'}
        res_dict = self.update_procedure_version_status(procedure_id, 3, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertEqual(res_dict['time_approved'], '')  
        self.assertEqual(res_dict['time_released'], '')  
        self.assertEqual(res_dict['institutional_release_id'], '')
        self.assertEqual(res_dict['status'], 'SUBMITTED')

        data = {'action': 'APPROVE'}
        res_dict = self.update_procedure_version_status(procedure_id, 3, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertTrue(len(res_dict['time_approved']) > 0)
        self.assertEqual(res_dict['time_released'], '')  
        self.assertEqual(res_dict['institutional_release_id'], '')
        self.assertEqual(res_dict['status'], 'APPROVED')

        res_dict = self.update_procedure_version(procedure_id, 3, {'institutional_release_id': 'Rev A'})
        data = {'action': 'RELEASE'}
        res_dict = self.update_procedure_version_status(procedure_id, 3, data)
        self.assertTrue(len(res_dict['time_submitted']) > 0)
        self.assertTrue(len(res_dict['time_approved']) > 0)
        self.assertTrue(len(res_dict['time_released']) > 0)
        self.assertEqual(res_dict['institutional_release_id'], 'Rev A')
        self.assertEqual(res_dict['status'], 'RELEASED')        
        
        
        structure_version_1 = self.get_version_structure(procedure_id, 3)
        self.assertEqual(structure_version_1['children'][0]['children'][1]['description'], 'Paragraph A Source')
        self.assertEqual(len(structure_version_1['children'][0]['children'][1]['tag_ids']), 2)
        self.assertNotEqual(structure_version_1['children'][0]['children'][1]['tag_ids'][0], tag_id_1)
        self.assertNotEqual(structure_version_1['children'][0]['children'][1]['tag_ids'][1], tag_id_2)
        
        #
        versions_data = self.export_procedure_versions(procedure_id, None, False, 200)
        logger.debug('versions_data=%s', json.dumps(versions_data, indent=4))
        self.assertEqual(versions_data['procedure_info']['procedure_id'], procedure_id)
        self.assertEqual(len(versions_data['version_infos']), 4)
        self.assertEqual(len(versions_data['elements']), 9)
        self.assertEqual(len(versions_data['edges']), 9)

        # 
        procedure_info = self.get_procedure(procedure_id)
        version_info_0 = self.get_procedure_version(procedure_id, 0)
        version_info_1 = self.get_procedure_version(procedure_id, 1)
        version_info_2 = self.get_procedure_version(procedure_id, 2)
        version_info_3 = self.get_procedure_version(procedure_id, 3)

        #
        structure_version_0 = self.get_version_structure(procedure_id, 0)
        structure_version_1 = self.get_version_structure(procedure_id, 1)
        structure_version_2 = self.get_version_structure(procedure_id, 2)
        structure_version_3 = self.get_version_structure(procedure_id, 3)

        ### delete versions
        self.delete_procedure_version(procedure_id, 1)
        self.delete_procedure_version(procedure_id, 2)

        # import procedure to restore
        self.import_procedure(versions_data, 200)

        # check procedure
        procedure_info_ = self.get_procedure(procedure_id)
        self.compare_procedure_info(procedure_info_, procedure_info)

        version_info_0_ = self.get_procedure_version(procedure_id, 0)
        version_info_1_ = self.get_procedure_version(procedure_id, 1)
        version_info_2_ = self.get_procedure_version(procedure_id, 2)
        version_info_3_ = self.get_procedure_version(procedure_id, 3)
        
        self.assertDictEqual(version_info_0, version_info_0_)
        self.assertDictEqual(version_info_1, version_info_1_)
        self.assertDictEqual(version_info_2, version_info_2_)
        self.assertDictEqual(version_info_3, version_info_3_)

        structure_version_0_ = self.get_version_structure(procedure_id, 0)
        structure_version_1_ = self.get_version_structure(procedure_id, 1)
        structure_version_2_ = self.get_version_structure(procedure_id, 2)
        structure_version_3_ = self.get_version_structure(procedure_id, 3)

        self.assertDictEqual(structure_version_0, structure_version_0_)
        self.assertDictEqual(structure_version_1, structure_version_1_)
        self.assertDictEqual(structure_version_2, structure_version_2_)
        self.assertDictEqual(structure_version_3, structure_version_3_)        

        ### delete procedure
        self.delete_procedure(procedure_id)

        ### import procedure
        self.import_procedure(versions_data, 200)
        
        # check procedure
        procedure_info_ = self.get_procedure(procedure_id)
        self.compare_procedure_info(procedure_info_, procedure_info)

        version_info_0_ = self.get_procedure_version(procedure_id, 0)
        version_info_1_ = self.get_procedure_version(procedure_id, 1)
        version_info_2_ = self.get_procedure_version(procedure_id, 2)
        version_info_3_ = self.get_procedure_version(procedure_id, 3)
        
        self.assertDictEqual(version_info_0, version_info_0_)
        self.assertDictEqual(version_info_1, version_info_1_)
        self.assertDictEqual(version_info_2, version_info_2_)
        self.assertDictEqual(version_info_3, version_info_3_)

        structure_version_0_ = self.get_version_structure(procedure_id, 0)
        structure_version_1_ = self.get_version_structure(procedure_id, 1)
        structure_version_2_ = self.get_version_structure(procedure_id, 2)
        structure_version_3_ = self.get_version_structure(procedure_id, 3)

        self.assertDictEqual(structure_version_0, structure_version_0_)
        self.assertDictEqual(structure_version_1, structure_version_1_)
        self.assertDictEqual(structure_version_2, structure_version_2_)
        self.assertDictEqual(structure_version_3, structure_version_3_)

        #
        versions_data_1 = self.export_procedure_versions(procedure_id, 1, False, 200)
        logger.debug('versions_data_1=%s', json.dumps(versions_data_1, indent=4))
        self.assertEqual(versions_data_1['procedure_info']['procedure_id'], procedure_id)
        self.assertEqual(len(versions_data_1['version_infos']), 1)
        self.assertEqual(versions_data_1['version_infos'][0]['version'], 1)
        self.assertEqual(len(versions_data_1['elements']), 1)
        self.assertEqual(len(versions_data_1['edges']), 1)

        versions_data_released = self.export_procedure_versions(procedure_id, None, True, 200)
        logger.debug('versions_data_released=%s', json.dumps(versions_data_released, indent=4))
        self.assertEqual(versions_data_released['procedure_info']['procedure_id'], procedure_id)
        self.assertEqual(len(versions_data_released['version_infos']), 2)
        self.assertEqual(versions_data_released['version_infos'][0]['version'], 1)
        self.assertEqual(versions_data_released['version_infos'][1]['version'], 3)
        self.assertEqual(len(versions_data_released['elements']), 4)
        self.assertEqual(len(versions_data_released['edges']), 4)        

        versions_data_3 = self.export_procedure_versions(procedure_id, 3, True, 200)
        logger.debug('versions_data_3_released=%s', json.dumps(versions_data_3, indent=4))
        self.assertEqual(versions_data_3['procedure_info']['procedure_id'], procedure_id)
        self.assertEqual(len(versions_data_3['version_infos']), 1)
        self.assertEqual(versions_data_3['version_infos'][0]['version'], 3)
        self.assertEqual(len(versions_data_3['elements']), 3)
        self.assertEqual(len(versions_data_3['edges']), 3)        

        ### delete procedure
        self.delete_procedure(procedure_id)

        ### import procedure
        self.import_procedure(versions_data_1, 200)
        
        # check procedure
        procedure_info_ = self.get_procedure(procedure_id)
        self.compare_procedure_info(procedure_info_, procedure_info)

        version_info_1_ = self.get_procedure_version(procedure_id, 1)
        self.assertDictEqual(version_info_1, version_info_1_)

        structure_version_1_ = self.get_version_structure(procedure_id, 1)
        self.assertDictEqual(structure_version_1, structure_version_1_)

        ### import procedure
        self.import_procedure(versions_data_released, 200)
        
        # check procedure
        procedure_info_ = self.get_procedure(procedure_id)
        self.compare_procedure_info(procedure_info_, procedure_info)

        version_info_1_ = self.get_procedure_version(procedure_id, 1)
        version_info_3_ = self.get_procedure_version(procedure_id, 3)
        self.assertDictEqual(version_info_1, version_info_1_)
        self.assertDictEqual(version_info_3, version_info_3_)        

        structure_version_1_ = self.get_version_structure(procedure_id, 1)
        structure_version_3_ = self.get_version_structure(procedure_id, 3)
        self.assertDictEqual(structure_version_1, structure_version_1_)
        self.assertDictEqual(structure_version_3, structure_version_3_)


    def test_procedure_outline(self):

        ## create source procedure
        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            description='Section 1')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='SIBLING',
            description='Section 2')

        section_2 = res['elem']
        section_2_id = section_2['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='CHILD',
            description='Paragraph 1-1')

        paragraph_1_1 = res['elem']
        paragraph_1_1_id = paragraph_1_1['elem_id']

        # add steps to section 1
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,        
            insert_after_id=paragraph_1_1_id,
            level='SIBLING',
            title='Step 1-2',
            description='Step 1-2')

        step_1_2 = res['elem']
        step_1_2_id = step_1_2['elem_id']

        #
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=step_1_2_id,
            level='SIBLING',
            title='Step 1-3',
            description='Step 1-3')

        step_1_3 = res['elem']
        step_1_3_id = step_1_3['elem_id']

        # add steps to section 2
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=section_2_id,
            level='CHILD',
            title='Step 2-1',
            description='Step 2-1')

        step_2_1 = res['elem']
        step_2_1_id = step_2_1['elem_id']

        #
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=step_2_1_id,
            level='SIBLING',
            title='Step 2-2',
            description='Step 2-2')

        step_2_2 = res['elem']
        step_2_2_id = step_2_2['elem_id']

        # add version
        version_dict = self.create_procedure_version(procedure_id, 'First version', 'hongmank')
        version = version_dict['version']
        self.assertEqual(version, 1)

        outline_elems = self.get_outline(procedure_url, version)

        logger.debug('outline_elems: %s', json.dumps(outline_elems, indent=4))

        self.assertEqual(len(outline_elems), 7)

        self.assertEqual(outline_elems[2]['title'], 'Step 1-2')
        self.assertEqual(outline_elems[2]['number'], '1-2')
        self.assertEqual(outline_elems[2]['selected'], True)

        self.assertEqual(outline_elems[6]['title'], 'Step 2-2')
        self.assertEqual(outline_elems[6]['number'], '2-2')
        self.assertEqual(outline_elems[6]['selected'], True)

    def test_circular_reference(self):

        ## p1
        title_1 = 'p1_' + random_string()
        procedure_dict = self.create_procedure(title_1, '', '', 'hongmank')
        procedure_id_1 = procedure_dict['procedure_id']
        procedure_url_1 = shared_dict['host'] + '/procedures/' + procedure_id_1

        procedure_section_data = {'elem_type': 'PROCEDURE_SECTION', 'description': "p1 refers to p3", 'title': ''}
        res = self.add_procedure_section(base_url=procedure_url_1,
            insert_after_id="-1",
            level='CHILD',
            procedure_section=procedure_section_data)
        procedure_section_id_1 = res['elem']['elem_id']    

        ## p2
        title_2 = 'p2_' + random_string()
        procedure_dict = self.create_procedure(title_2, '', '', 'hongmank')
        procedure_id_2 = procedure_dict['procedure_id']
        procedure_url_2 = shared_dict['host'] + '/procedures/' + procedure_id_2
        procedure_section_data = {'elem_type': 'PROCEDURE_SECTION', 'description': "p2 refers to p1", 'title': ''}
        res = self.add_procedure_section(base_url=procedure_url_2,
            insert_after_id="-1",
            level='CHILD',
            procedure_section=procedure_section_data)
        procedure_section_id_2 = res['elem']['elem_id']    
        procedure_section_input = {
            'reference_procedure_id': procedure_id_1,
            'reference_procedure_title': title_1,              
            'reference_procedure_version': 0,
            'reference_procedure_version_description': '',
            'elements': [{
                'elem_id': procedure_section_id_1,
                'elem_type': 'PROCEDURE_SECTION',
                'selected': True,
                'number': '1'
            }]
        }
        self.update_procedure_section_input(procedure_url_2, procedure_section_id_2, procedure_section_input)

        ## p3
        title_3 = 'p3_' + random_string()
        procedure_dict = self.create_procedure(title_3, '', '', 'hongmank')
        procedure_id_3 = procedure_dict['procedure_id']
        procedure_url_3 = shared_dict['host'] + '/procedures/' + procedure_id_3
        procedure_section_data = {'elem_type': 'PROCEDURE_SECTION', 'description': "p3 refers to p2", 'title': ''}
        res = self.add_procedure_section(base_url=procedure_url_3,
            insert_after_id="-1",
            level='CHILD',
            procedure_section=procedure_section_data)
        procedure_section_id_3 = res['elem']['elem_id']    
        procedure_section_input = {
            'reference_procedure_id': procedure_id_2,
            'reference_procedure_title': title_2,              
            'reference_procedure_version': 0,
            'reference_procedure_version_description': '',
            'elements': [{
                'elem_id': procedure_section_id_2,
                'elem_type': 'PROCEDURE_SECTION',
                'selected': True,
                'number': '1'
            }]
        }
        self.update_procedure_section_input(procedure_url_3, procedure_section_id_3, procedure_section_input)

        ## Try to create a circular reference 
        procedure_section_input = {
            'reference_procedure_id': procedure_id_1,
            'reference_procedure_title': title_1,              
            'reference_procedure_version': 0,
            'reference_procedure_version_description': '',
            'elements': [{
                'elem_id': procedure_section_id_1,
                'elem_type': 'PROCEDURE_SECTION',
                'selected': True,
                'number': '1'
            }]
        }
        self.update_procedure_section_input(procedure_url_1, procedure_section_id_1, procedure_section_input, code_expected=400)

        ## Try to create a circular reference
        # OK with no elements
        procedure_section_input = {
            'reference_procedure_id': procedure_id_3,
            'reference_procedure_title': title_3,              
            'reference_procedure_version': 0,
            'reference_procedure_version_description': '',
            'elements': []
        }
        self.update_procedure_section_input(procedure_url_1, procedure_section_id_1, procedure_section_input, code_expected=204)

        procedure_section_input = {
            'reference_procedure_id': procedure_id_3,
            'reference_procedure_title': title_3,              
            'reference_procedure_version': 0,
            'reference_procedure_version_description': '',
            'elements': [{
                'elem_id': procedure_section_id_3,
                'elem_type': 'PROCEDURE_SECTION',
                'selected': True,
                'number': '1'
            }]
        }
        self.update_procedure_section_input(procedure_url_1, procedure_section_id_1, procedure_section_input, code_expected=400)


        ## Try to create a circular reference
        # OK with no elements
        procedure_section_input = {
            'reference_procedure_id': procedure_id_3,
            'reference_procedure_title': title_3,              
            'reference_procedure_version': 0,
            'reference_procedure_version_description': '',
            'elements': []
        }
        self.update_procedure_section_input(procedure_url_1, procedure_section_id_1, procedure_section_input, code_expected=204)

        procedure_section_input = {
            'reference_procedure_id': procedure_id_3,
            'reference_procedure_title': title_3,              
            'reference_procedure_version': 0,
            'reference_procedure_version_description': '',
            'elements': [{
                'elem_id': procedure_section_id_3,
                'elem_type': 'PROCEDURE_SECTION',
                'selected': True,
                'number': '1'
            }]
        }
        self.update_procedure_section_input(procedure_url_1, procedure_section_id_1, procedure_section_input, code_expected=400)

        ## Try to create a circular reference (between two. Check this after checking dependencies among three procs)
        # OK with no elements
        procedure_section_input = {
            'reference_procedure_id': procedure_id_3,
            'reference_procedure_title': title_3,              
            'reference_procedure_version': 0,
            'reference_procedure_version_description': '',
            'elements': []
        }
        self.update_procedure_section_input(procedure_url_2, procedure_section_id_2, procedure_section_input, code_expected=204)

        procedure_section_input = {
            'reference_procedure_id': procedure_id_3,
            'reference_procedure_title': title_3,              
            'reference_procedure_version': 0,
            'reference_procedure_version_description': '',
            'elements': [{
                'elem_id': procedure_section_id_3,
                'elem_type': 'PROCEDURE_SECTION',
                'selected': True,
                'number': '1'
            }]
        }
        self.update_procedure_section_input(procedure_url_2, procedure_section_id_2, procedure_section_input, code_expected=400)


    def test_invalid_http_method(self):
        url = shared_dict['host'] + '/procedures'
        result = requests.delete(url, headers=shared_dict['headers'])

        self.assertEqual(result.status_code, 405)

        # should not have crashed service
        # check a few times in case there are replicated services
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)

    def export_procedure_versions(self, procedure_id, version, released_only, code_expected=200):
        url = '{0}/procedures/{1}/export_versions'.format(shared_dict['host'], procedure_id)
        
        params = {}
        if version is not None:
            params['version'] = version
        if released_only is not None:
            params['released_only'] = 'true' if released_only else 'false'

        logger.debug('GET: %s', url)

        result = requests.get(url,
            params = params,
            headers=shared_dict['headers'])

        self.assertEqual(result.status_code, code_expected)

        res_dict = json.loads(result.text)

        return res_dict

    def import_procedure(self, import_input, code_expected=200):
        url = '{0}/procedures/import'.format(shared_dict['host'])
        logger.debug('GET: %s', url)
        result = requests.post(url,
            json = import_input,
            headers=shared_dict['headers'])

        self.assertEqual(result.status_code, code_expected)

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./test-reports/"))
