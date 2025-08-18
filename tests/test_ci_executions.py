"""
Usage:
 - Run all tests
   $ python executions_test.py

 - Run a class
   $ python executions_test.py ExecutionsTest

 - Run a method
   $ python executions_test.py ExecutionDeleteTest.test_delete_executions

"""
import xmlrunner
import os
import sys
import unittest
import requests
import json
import random
import time
import string
from dateutil import parser
from datetime import datetime
import math
import dateutil.tz
from config import shared_dict, logger
from test_utils import random_string
from ingenium_client import CoreTestBase, StepTypes


class ExecutionsTest(CoreTestBase):
    def test_create_execution(self):
        logger.debug('test_create_execution')

        id_dict = self.create_execution_example()
        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        ## Get As Run
        res_dict = self.get_as_run(execution_id)
        logger.debug('as_run res_dict= %s', json.dumps(res_dict, indent=4))

        self.check_as_run(res_dict)


        ## Test for getting steps
        self.run_get_elements(execution_id)

        ## Get As Run
        res_dict = self.get_as_run(execution_id)
        logger.debug('as_run res_dict= %s', json.dumps(res_dict, indent=4))

        self.check_as_run(res_dict)

        self.run_move_elements(id_dict)

    def test_copy_element(self):
        logger.debug('test_copy_element')

        id_dict = self.create_execution_example()
        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        self.run_copy_element(id_dict)        

    def test_copy_elements(self):
        id_dict = self.create_execution_example()
        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        ## copy a step
        res_dict = self.copy_elements(base_url=execution_url,
            elem_ids=[step_id_1_1, step_id_3_1], insert_after_id=section_id_3, level='CHILD',
            code_expected=200)
        
        logger.debug('copy_element res: %s', json.dumps(res_dict, indent=4))            
        
        self.assertEqual(len(res_dict['numbers']), 4)
        self.assertEqual(res_dict['numbers'][0]['number'], "3-1")
        self.assertEqual(res_dict['numbers'][1]['number'], "3-2")
        self.assertEqual(res_dict['numbers'][2]['number'], "3-3")
        self.assertEqual(res_dict['numbers'][3]['number'], "3-4")

        self.assertEqual(len(res_dict['elements']), 2)
        self.assertEqual(res_dict['elements'][0]['title'], 'Step 1-1')
        self.assertEqual(res_dict['elements'][0]['number'], '3-1')
        self.assertEqual(res_dict['elements'][1]['title'], 'Step 3-1')
        self.assertEqual(res_dict['elements'][1]['number'], '3-2')         

        res_dict = self.get_elements(execution_url)
        logger.debug('copied step elements res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 9)
        self.assertEqual(res_dict[0]['title'], "Section 1")
        self.assertEqual(res_dict[1]['title'], "Step 1-1")
        self.assertEqual(res_dict[2]['title'], "Step 1-2")
        self.assertEqual(res_dict[3]['title'], 'Paragraph Section 1')
        self.assertEqual(res_dict[4]['title'], "Section 3")
        self.assertEqual(res_dict[5]['title'], "Step 1-1")        
        self.assertEqual(res_dict[6]['title'], "Step 3-1") 
        self.assertEqual(res_dict[7]['title'], "Step 3-1")
        self.assertEqual(res_dict[8]['title'], "Step 3-2")

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "2")
        self.assertEqual(res_dict[4]['number'], "3")
        self.assertEqual(res_dict[5]['number'], "3-1")
        self.assertEqual(res_dict[6]['number'], "3-2")
        self.assertEqual(res_dict[7]['number'], "3-3")   
        self.assertEqual(res_dict[8]['number'], "3-4")     

    def test_copy_element_across_executions(self):
        logger.debug('test_copy_element_across_executions')

        source_id_dict = self.create_execution_example()
        source_execution_url = source_id_dict['execution_url']
        source_execution_id = source_id_dict['execution_id']
        source_section_id_1 = source_id_dict['section_id_1']
        source_step_id_1_1 = source_id_dict['step_id_1_1']
        source_step_id_1_2 = source_id_dict['step_id_1_2']
        source_section_id_3 = source_id_dict['section_id_3']
        source_step_id_3_1 = source_id_dict['step_id_3_1']
        source_step_id_3_2 = source_id_dict['step_id_3_2']

        target_id_dict = self.create_execution_example()
        target_execution_url = target_id_dict['execution_url']
        target_execution_id = target_id_dict['execution_id']
        target_section_id_1 = target_id_dict['section_id_1']
        target_step_id_1_1 = target_id_dict['step_id_1_1']
        target_step_id_1_2 = target_id_dict['step_id_1_2']
        target_section_id_3 = target_id_dict['section_id_3']
        target_step_id_3_1 = target_id_dict['step_id_3_1']
        target_step_id_3_2 = target_id_dict['step_id_3_2']        

        res_dict = self.copy_element_across(target_execution_url, source_section_id_1, target_section_id_1, 'SIBLING', 
            source_execution_id, None, None)
        logger.debug('element copied res_dict: %s', json.dumps(res_dict, indent=4))            

        added_elements = res_dict['elements']
        self.assertEqual(len(added_elements), 3)

        for added_element in added_elements:
            self.assertEqual(added_element['execution_id'], target_execution_id)

        numbers = res_dict['numbers']
        self.assertEqual(len(numbers), 7)

        self.assertEqual(numbers[0]['number'], '2')
        self.assertEqual(numbers[1]['number'], '2-1')
        self.assertEqual(numbers[2]['number'], '2-2')
        self.assertEqual(numbers[3]['number'], '3')
        self.assertEqual(numbers[4]['number'], '4')
        self.assertEqual(numbers[5]['number'], '4-1')
        self.assertEqual(numbers[6]['number'], '4-2')                  

        elements = self.get_elements(target_execution_url)
        logger.debug('after copy elements elements= %s', json.dumps(elements, indent=4))   

        self.assertEqual(len(elements), 10)

        for element in elements:
            self.assertEqual(element['execution_id'], target_execution_id)    

        self.assertEqual(elements[0]['number'], '1')
        self.assertEqual(elements[1]['number'], '1-1')
        self.assertEqual(elements[2]['number'], '1-2')
        self.assertEqual(elements[3]['number'], '2')
        self.assertEqual(elements[4]['number'], '2-1')
        self.assertEqual(elements[5]['number'], '2-2')
        self.assertEqual(elements[6]['number'], '3')
        self.assertEqual(elements[7]['number'], '4')
        self.assertEqual(elements[8]['number'], '4-1')
        self.assertEqual(elements[9]['number'], '4-2')     

    def test_copy_elements_across_executions(self):
        logger.debug('test_copy_elements_across_executions')

        source_id_dict = self.create_execution_example()
        source_execution_url = source_id_dict['execution_url']
        source_execution_id = source_id_dict['execution_id']
        source_section_id_1 = source_id_dict['section_id_1']
        source_step_id_1_1 = source_id_dict['step_id_1_1']
        source_step_id_1_2 = source_id_dict['step_id_1_2']
        source_section_id_3 = source_id_dict['section_id_3']
        source_step_id_3_1 = source_id_dict['step_id_3_1']
        source_step_id_3_2 = source_id_dict['step_id_3_2']

        target_id_dict = self.create_execution_example()
        target_execution_url = target_id_dict['execution_url']
        target_execution_id = target_id_dict['execution_id']
        target_section_id_1 = target_id_dict['section_id_1']
        target_step_id_1_1 = target_id_dict['step_id_1_1']
        target_step_id_1_2 = target_id_dict['step_id_1_2']
        target_section_id_3 = target_id_dict['section_id_3']
        target_step_id_3_1 = target_id_dict['step_id_3_1']
        target_step_id_3_2 = target_id_dict['step_id_3_2']        

        res_dict = self.copy_elements_across(target_execution_url, [source_section_id_1, source_step_id_3_1], target_section_id_1, 'SIBLING', 
            source_execution_id, None, None)
        logger.debug('element copied res_dict: %s', json.dumps(res_dict, indent=4))            

        added_elements = res_dict['elements']
        self.assertEqual(len(added_elements), 4)

        for added_element in added_elements:
            self.assertEqual(added_element['execution_id'], target_execution_id)

        numbers = res_dict['numbers']
        self.assertEqual(len(numbers), 8)

        self.assertEqual(numbers[0]['number'], '2')
        self.assertEqual(numbers[1]['number'], '2-1')
        self.assertEqual(numbers[2]['number'], '2-2')
        self.assertEqual(numbers[3]['number'], '3')
        self.assertEqual(numbers[4]['number'], '4')
        self.assertEqual(numbers[5]['number'], '5')
        self.assertEqual(numbers[6]['number'], '5-1')
        self.assertEqual(numbers[7]['number'], '5-2')                  

        elements = self.get_elements(target_execution_url)
        logger.debug('after copy elements elements= %s', json.dumps(elements, indent=4))   

        self.assertEqual(len(elements), 11)

        for element in elements:
            self.assertEqual(element['execution_id'], target_execution_id)    

        self.assertEqual(elements[0]['number'], '1')
        self.assertEqual(elements[1]['number'], '1-1')
        self.assertEqual(elements[2]['number'], '1-2')
        self.assertEqual(elements[3]['number'], '2')
        self.assertEqual(elements[4]['number'], '2-1')
        self.assertEqual(elements[5]['number'], '2-2')
        self.assertEqual(elements[6]['number'], '3')
        self.assertEqual(elements[7]['number'], '4')
        self.assertEqual(elements[8]['number'], '5')
        self.assertEqual(elements[9]['number'], '5-1')
        self.assertEqual(elements[10]['number'], '5-2')     

    def test_copy_from_procedure_to_execution(self):
        logger.debug('test_copy_from_procedure_to_execution')

        source_id_dict = self.create_procedure_example()
        source_procedure_id = source_id_dict['procedure_id']
        source_procedure_url = source_id_dict['procedure_url']
        source_procedure_title = source_id_dict['procedure_title']
        source_version = source_id_dict['version']
        source_version_description = source_id_dict['version_description']
        source_section_1_id = source_id_dict['section_1_id']
        source_paragraph_1_1_id = source_id_dict['paragraph_1_1_id']
        source_step_1_2_id = source_id_dict['step_1_2_id']
        source_step_1_3_id = source_id_dict['step_1_3_id']
        source_section_2_id = source_id_dict['section_2_id']
        source_step_2_1_id = source_id_dict['step_2_1_id']
        source_step_2_2_id = source_id_dict['step_2_2_id']

        target_id_dict = self.create_execution_example()
        target_execution_url = target_id_dict['execution_url']
        target_execution_id = target_id_dict['execution_id']
        target_section_id_1 = target_id_dict['section_id_1']
        target_step_id_1_1 = target_id_dict['step_id_1_1']
        target_step_id_1_2 = target_id_dict['step_id_1_2']
        target_section_id_3 = target_id_dict['section_id_3']
        target_step_id_3_1 = target_id_dict['step_id_3_1']
        target_step_id_3_2 = target_id_dict['step_id_3_2']        

        res_dict = self.copy_element_across(target_execution_url, source_section_1_id, target_section_id_1, 'SIBLING', 
            None, source_procedure_id, source_version)
        logger.debug('element copied res_dict: %s', json.dumps(res_dict, indent=4))            

        added_elements = res_dict['elements']
        self.assertEqual(len(added_elements), 4)

        for added_element in added_elements:
            self.assertEqual(added_element['execution_id'], target_execution_id)
            self.assertEqual(added_element['procedure_id'], '')

        numbers = res_dict['numbers']
        self.assertEqual(len(numbers), 8)

        self.assertEqual(numbers[0]['number'], '2')
        self.assertEqual(numbers[1]['number'], '2-1')
        self.assertEqual(numbers[2]['number'], '2-2')
        self.assertEqual(numbers[3]['number'], '2-3')
        self.assertEqual(numbers[4]['number'], '3')
        self.assertEqual(numbers[5]['number'], '4')
        self.assertEqual(numbers[6]['number'], '4-1')
        self.assertEqual(numbers[7]['number'], '4-2')                  

        elements = self.get_elements(target_execution_url)
        logger.debug('after copy elements elements= %s', json.dumps(elements, indent=4))   

        self.assertEqual(len(elements), 11)

        for element in elements:
            self.assertEqual(element['execution_id'], target_execution_id)   
            self.assertEqual(added_element['procedure_id'], '') 

        self.assertEqual(elements[0]['number'], '1')
        self.assertEqual(elements[1]['number'], '1-1')
        self.assertEqual(elements[2]['number'], '1-2')
        self.assertEqual(elements[3]['number'], '2')
        self.assertEqual(elements[4]['number'], '2-1')
        self.assertEqual(elements[5]['number'], '2-2')
        self.assertEqual(elements[6]['number'], '2-3')
        self.assertEqual(elements[7]['number'], '3')
        self.assertEqual(elements[8]['number'], '4')
        self.assertEqual(elements[9]['number'], '4-1')
        self.assertEqual(elements[10]['number'], '4-2')                     

    def test_copy_from_execution_to_procedure(self):
        logger.debug('test_copy_from_execution_to_procedure')

        source_id_dict = self.create_execution_example()
        source_execution_url = source_id_dict['execution_url']
        source_execution_id = source_id_dict['execution_id']
        source_section_id_1 = source_id_dict['section_id_1']
        source_step_id_1_1 = source_id_dict['step_id_1_1']
        source_step_id_1_2 = source_id_dict['step_id_1_2']
        source_section_id_3 = source_id_dict['section_id_3']
        source_step_id_3_1 = source_id_dict['step_id_3_1']
        source_step_id_3_2 = source_id_dict['step_id_3_2']          

        target_id_dict = self.create_procedure_example()
        target_procedure_id = target_id_dict['procedure_id']
        target_procedure_url = target_id_dict['procedure_url']
        target_procedure_title = target_id_dict['procedure_title']
        target_version = target_id_dict['version']
        target_version_description = target_id_dict['version_description']
        target_section_1_id = target_id_dict['section_1_id']
        target_paragraph_1_1_id = target_id_dict['paragraph_1_1_id']
        target_step_1_2_id = target_id_dict['step_1_2_id']
        target_step_1_3_id = target_id_dict['step_1_3_id']
        target_section_2_id = target_id_dict['section_2_id']
        target_step_2_1_id = target_id_dict['step_2_1_id']
        target_step_2_2_id = target_id_dict['step_2_2_id']

        res_dict = self.copy_element_across(target_procedure_url, source_section_id_1, target_section_1_id, 'SIBLING', 
            source_execution_id, None, None)
        logger.debug('element copied res_dict: %s', json.dumps(res_dict, indent=4))            

        added_elements = res_dict['elements']
        self.assertEqual(len(added_elements), 3)

        for added_element in added_elements:
            self.assertEqual(added_element['execution_id'], '')
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

        self.assertEqual(len(elements), 10)

        for element in elements:
            self.assertEqual(element['execution_id'], '')
            self.assertEqual(added_element['procedure_id'], target_procedure_id)

        self.assertEqual(elements[0]['number'], '1')
        self.assertEqual(elements[1]['number'], '1-1')
        self.assertEqual(elements[2]['number'], '1-2')
        self.assertEqual(elements[3]['number'], '1-3')
        self.assertEqual(elements[4]['number'], '2')        
        self.assertEqual(elements[5]['number'], '2-1')
        self.assertEqual(elements[6]['number'], '2-2')
        self.assertEqual(elements[7]['number'], '3')
        self.assertEqual(elements[8]['number'], '3-1')
        self.assertEqual(elements[9]['number'], '3-2') 

    def run_move_elements(self, id_dict):
        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        paragraph_id_2 = id_dict['paragraph_id_2']

        ## Move element

        res_dict = self.move_element(base_url=execution_url,
            elem_id=section_id_3, insert_after_id='-1', level='CHILD',
            code_expected=200)

        logger.debug('element moved: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 7)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_id_3)
        self.assertEqual(res_dict['numbers'][0]['number'], '1')        
        self.assertEqual(res_dict['numbers'][1]['elem_id'], step_id_3_1)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-1')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], step_id_3_2)
        self.assertEqual(res_dict['numbers'][2]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], section_id_1)
        self.assertEqual(res_dict['numbers'][3]['number'], '2')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], step_id_1_1)
        self.assertEqual(res_dict['numbers'][4]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][5]['elem_id'], step_id_1_2)
        self.assertEqual(res_dict['numbers'][5]['number'], '2-2')
        self.assertEqual(res_dict['numbers'][6]['elem_id'], paragraph_id_2)
        self.assertEqual(res_dict['numbers'][6]['number'], '3')        

        self.assertEqual(len(res_dict['elem_ids']), 7)
        self.assertEqual(res_dict['elem_ids'][0], section_id_3)
        self.assertEqual(res_dict['elem_ids'][1], step_id_3_1)
        self.assertEqual(res_dict['elem_ids'][2], step_id_3_2)
        self.assertEqual(res_dict['elem_ids'][3], section_id_1)
        self.assertEqual(res_dict['elem_ids'][4], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][5], step_id_1_2)
        self.assertEqual(res_dict['elem_ids'][6], paragraph_id_2)


        res_dict = self.get_as_run(execution_id)
        logger.debug('moved as_run res_dict= %s', json.dumps(res_dict, indent=4))

        # move it back

        res_dict = self.move_element(base_url=execution_url,
            elem_id=section_id_3, insert_after_id=paragraph_id_2, level='SIBLING',
            code_expected=200)

        logger.debug('element moved: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 7)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_id_1)
        self.assertEqual(res_dict['numbers'][0]['number'], '1')        
        self.assertEqual(res_dict['numbers'][1]['elem_id'], step_id_1_1)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-1')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], step_id_1_2)
        self.assertEqual(res_dict['numbers'][2]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], paragraph_id_2)
        self.assertEqual(res_dict['numbers'][3]['number'], '2')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], section_id_3)
        self.assertEqual(res_dict['numbers'][4]['number'], '3')
        self.assertEqual(res_dict['numbers'][5]['elem_id'], step_id_3_1)
        self.assertEqual(res_dict['numbers'][5]['number'], '3-1')
        self.assertEqual(res_dict['numbers'][6]['elem_id'], step_id_3_2)
        self.assertEqual(res_dict['numbers'][6]['number'], '3-2')   

        res_dict = self.get_as_run(execution_id)
        logger.debug('moved back as_run res_dict= %s', json.dumps(res_dict, indent=4))


        res_dict = self.move_element(base_url=execution_url,
            elem_id=step_id_1_1, insert_after_id=section_id_3, level='CHILD',
            code_expected=200)

        logger.debug('element moved: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 4)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_id_1_2)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-1')        
        self.assertEqual(res_dict['numbers'][1]['elem_id'], step_id_1_1)
        self.assertEqual(res_dict['numbers'][1]['number'], '3-1')        
        self.assertEqual(res_dict['numbers'][2]['elem_id'], step_id_3_1)
        self.assertEqual(res_dict['numbers'][2]['number'], '3-2')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], step_id_3_2)
        self.assertEqual(res_dict['numbers'][3]['number'], '3-3')


        ## Get As Run to check
        url = shared_dict['host'] + '/executions/' + execution_id + '/as_run'
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('as_run res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(res_dict['children'][0]['title'], 'Section 1')
        self.assertEqual(res_dict['children'][0]['number'], '1')
        self.assertEqual(res_dict['children'][0]['children'][0]['title'], 'Step 1-2')
        self.assertEqual(res_dict['children'][0]['children'][0]['number'], '1-1')

        self.assertEqual(res_dict['children'][1]['title'], 'Paragraph Section 1')
        self.assertEqual(res_dict['children'][1]['number'], '2')

        self.assertEqual(res_dict['children'][2]['title'], 'Section 3')
        self.assertEqual(res_dict['children'][2]['number'], '3')
        self.assertEqual(res_dict['children'][2]['children'][0]['title'], 'Step 1-1')
        self.assertEqual(res_dict['children'][2]['children'][0]['number'], '3-1')
        self.assertEqual(res_dict['children'][2]['children'][1]['title'], 'Step 3-1')
        self.assertEqual(res_dict['children'][2]['children'][1]['number'], '3-2')
        self.assertEqual(res_dict['children'][2]['children'][2]['title'], 'Step 3-2')
        self.assertEqual(res_dict['children'][2]['children'][2]['number'], '3-3')

        ## move back the element
        res_dict = self.move_element(base_url=execution_url,
            elem_id=step_id_1_1, insert_after_id=section_id_1, level='CHILD',
            code_expected=200)

        logger.debug('element moved: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 4)

        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_id_1_1)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-1')  
        self.assertEqual(res_dict['numbers'][1]['elem_id'], step_id_1_2)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-2')        
        self.assertEqual(res_dict['numbers'][2]['elem_id'], step_id_3_1)
        self.assertEqual(res_dict['numbers'][2]['number'], '3-1')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], step_id_3_2)
        self.assertEqual(res_dict['numbers'][3]['number'], '3-2')

        ## Get As Run to check
        url = shared_dict['host'] + '/executions/' + execution_id + '/as_run'
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('as_run res_dict= %s', json.dumps(res_dict, indent=4))

        self.check_as_run(res_dict)

        #### insert an element and check numbers

        ## Add a section temporarily
        res_dict = self.add_section(base_url=execution_url,
            insert_after_id=section_id_1,
            level='SIBLING',
            title='Section 1 temp')

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))

        section_id_1_temp = res_dict['elem']['elem_id']
        self.assertEqual(res_dict['elem']['number'], '2')

        # check numbers
        self.assertEqual(len(res_dict['numbers']), 5)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_id_1_temp)
        self.assertEqual(res_dict['numbers'][0]['number'], '2')          
        self.assertEqual(res_dict['numbers'][1]['elem_id'], paragraph_id_2)
        self.assertEqual(res_dict['numbers'][1]['number'], '3')  
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_id_3)
        self.assertEqual(res_dict['numbers'][2]['number'], '4')        
        self.assertEqual(res_dict['numbers'][3]['elem_id'], step_id_3_1)
        self.assertEqual(res_dict['numbers'][3]['number'], '4-1')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], step_id_3_2)
        self.assertEqual(res_dict['numbers'][4]['number'], '4-2')


        #### delete the dummy element and check numbers and as run
        res_dict = self.delete_element(execution_url, section_id_1_temp)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 4)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], paragraph_id_2)
        self.assertEqual(res_dict['numbers'][0]['number'], '2')  
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_id_3)
        self.assertEqual(res_dict['numbers'][1]['number'], '3')        
        self.assertEqual(res_dict['numbers'][2]['elem_id'], step_id_3_1)
        self.assertEqual(res_dict['numbers'][2]['number'], '3-1')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], step_id_3_2)
        self.assertEqual(res_dict['numbers'][3]['number'], '3-2')

        #### delete an element and check numbers and as run
        res_dict = self.delete_element(execution_url, step_id_1_1)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))

        # check numbers
        self.assertEqual(len(res_dict['numbers']), 1)      
        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_id_1_2)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-1')

        #### delete an element and check numbers and as run
        res_dict = self.delete_element(execution_url, section_id_1)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))

        # check numbers
        self.assertEqual(len(res_dict['numbers']), 4)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], paragraph_id_2)
        self.assertEqual(res_dict['numbers'][0]['number'], '1')  
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_id_3)
        self.assertEqual(res_dict['numbers'][1]['number'], '2')        
        self.assertEqual(res_dict['numbers'][2]['elem_id'], step_id_3_1)
        self.assertEqual(res_dict['numbers'][2]['number'], '2-1')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], step_id_3_2)
        self.assertEqual(res_dict['numbers'][3]['number'], '2-2')


    def run_copy_element(self, id_dict):
        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        paragraph_id_2 = id_dict['paragraph_id_2']
        
        # Add comment
        content = 'This is the first comment for the section'
        res_dict = self.add_conversation(execution_url, section_id_3, {'type': 'ACTIVITY_REPORT_COMMENT'})
        conversation_id = res_dict['conversation_id']
        comment = res_dict['comments'][0]
        comment_id = comment['comment_id']        
        res_dict = self.update_comment(execution_url, section_id_3, conversation_id, comment_id, content)
        self.assertEqual(res_dict['content'], content)
                
        ## Copy element
        res_dict = self.copy_element(base_url=execution_url,
            elem_id=section_id_3, insert_after_id='-1', level='CHILD',
            code_expected=200)
        # logger.debug('copy_element res: %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict['elements']), 3)
        self.assertEqual(res_dict['elements'][0]['title'], 'Section 3')
        self.assertEqual(res_dict['elements'][1]['title'], 'Step 3-1')
        self.assertEqual(res_dict['elements'][2]['title'], 'Step 3-2')
        
        # check comment
        self.assertEqual(len(res_dict['elements'][0]['conversations']), 0)        

        self.assertEqual(len(res_dict['numbers']), 10)
        self.assertEqual(res_dict['numbers'][0]['number'], "1")
        self.assertEqual(res_dict['numbers'][1]['number'], "1-1")
        self.assertEqual(res_dict['numbers'][2]['number'], "1-2")
        self.assertEqual(res_dict['numbers'][3]['number'], "2")
        self.assertEqual(res_dict['numbers'][4]['number'], "2-1")
        self.assertEqual(res_dict['numbers'][5]['number'], "2-2")
        self.assertEqual(res_dict['numbers'][6]['number'], "3")
        self.assertEqual(res_dict['numbers'][7]['number'], "4")
        self.assertEqual(res_dict['numbers'][8]['number'], "4-1")
        self.assertEqual(res_dict['numbers'][9]['number'], "4-2")        

        self.assertEqual(len(res_dict['elem_ids']), 10)
        self.assertEqual(res_dict['elem_ids'][0], res_dict['elements'][0]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][1], res_dict['elements'][1]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][2], res_dict['elements'][2]['elem_id'])
        self.assertEqual(res_dict['elem_ids'][3], section_id_1)
        self.assertEqual(res_dict['elem_ids'][4], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][5], step_id_1_2)
        self.assertEqual(res_dict['elem_ids'][6], paragraph_id_2)
        self.assertEqual(res_dict['elem_ids'][7], section_id_3)
        self.assertEqual(res_dict['elem_ids'][8], step_id_3_1)
        self.assertEqual(res_dict['elem_ids'][9], step_id_3_2)

        res_dict = self.get_elements(execution_url)
        logger.debug('copied elements res_dict= %s', json.dumps(res_dict, indent=4))        

        self.assertEqual(len(res_dict), 10)
        self.assertEqual(res_dict[0]['title'], "Section 3")
        self.assertEqual(res_dict[1]['title'], "Step 3-1")
        self.assertEqual(res_dict[2]['title'], "Step 3-2")
        self.assertEqual(res_dict[3]['title'], "Section 1")
        self.assertEqual(res_dict[4]['title'], "Step 1-1")
        self.assertEqual(res_dict[5]['title'], "Step 1-2")
        self.assertEqual(res_dict[6]['title'], 'Paragraph Section 1')
        self.assertEqual(res_dict[7]['title'], "Section 3")
        self.assertEqual(res_dict[8]['title'], "Step 3-1")
        self.assertEqual(res_dict[9]['title'], "Step 3-2")

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "2")
        self.assertEqual(res_dict[4]['number'], "2-1")
        self.assertEqual(res_dict[5]['number'], "2-2")
        self.assertEqual(res_dict[6]['number'], "3")
        self.assertEqual(res_dict[7]['number'], "4")
        self.assertEqual(res_dict[8]['number'], "4-1")
        self.assertEqual(res_dict[9]['number'], "4-2")
        
        # check comment
        
        self.assertEqual(len(res_dict[0]['conversations']), 0)
        self.assertEqual('comments' in res_dict[0], False)
        
        self.assertEqual(len(res_dict[7]['conversations']), 1)
        self.assertEqual(len(res_dict[7]['conversations'][0]['comments']), 1)
        self.assertEqual('comments' in res_dict[7], False)

        # delete the copied element

        copied_section_id_2 = res_dict[0]['elem_id']

        res_dict = self.delete_element(base_url=execution_url, elem_id=copied_section_id_2)

        logger.debug('element deleted: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 7)
        self.assertEqual(len(res_dict['elem_ids']), 7)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)
        self.assertEqual(res_dict['elem_ids'][1], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][2], step_id_1_2)
        self.assertEqual(res_dict['elem_ids'][3], paragraph_id_2)
        self.assertEqual(res_dict['elem_ids'][4], section_id_3)
        self.assertEqual(res_dict['elem_ids'][5], step_id_3_1)
        self.assertEqual(res_dict['elem_ids'][6], step_id_3_2)

        res_dict = self.get_elements(execution_url)
        logger.debug('deleted back elements res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 7)
        self.assertEqual(res_dict[0]['title'], "Section 1") 
        self.assertEqual(res_dict[1]['title'], "Step 1-1")
        self.assertEqual(res_dict[2]['title'], "Step 1-2")
        self.assertEqual(res_dict[3]['title'], 'Paragraph Section 1')
        self.assertEqual(res_dict[4]['title'], "Section 3")
        self.assertEqual(res_dict[5]['title'], "Step 3-1")
        self.assertEqual(res_dict[6]['title'], "Step 3-2")

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "2")
        self.assertEqual(res_dict[4]['number'], "3")
        self.assertEqual(res_dict[5]['number'], "3-1")
        self.assertEqual(res_dict[6]['number'], "3-2")

        ## copy a step

        res_dict = self.copy_element(base_url=execution_url,
            elem_id=step_id_1_1, insert_after_id=section_id_3, level='CHILD',
            code_expected=200)
        
        logger.debug('copy_element res: %s', json.dumps(res_dict, indent=4))            
        
        self.assertEqual(len(res_dict['numbers']), 3)
        self.assertEqual(res_dict['numbers'][0]['number'], "3-1")
        self.assertEqual(res_dict['numbers'][1]['number'], "3-2")
        self.assertEqual(res_dict['numbers'][2]['number'], "3-3")

        self.assertEqual(len(res_dict['elements']), 1)
        self.assertEqual(res_dict['elements'][0]['title'], 'Step 1-1')
        self.assertEqual(res_dict['elements'][0]['number'], '3-1')

        #res_dict = self.get_as_run(execution_id)
        #logger.debug('copy step as run after res_dict= %s', json.dumps(res_dict, indent=4))            

        res_dict = self.get_elements(execution_url)
        logger.debug('copied step elements res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 8)
        self.assertEqual(res_dict[0]['title'], "Section 1")
        self.assertEqual(res_dict[1]['title'], "Step 1-1")
        self.assertEqual(res_dict[2]['title'], "Step 1-2")
        self.assertEqual(res_dict[3]['title'], 'Paragraph Section 1')
        self.assertEqual(res_dict[4]['title'], "Section 3")
        self.assertEqual(res_dict[5]['title'], "Step 1-1")        
        self.assertEqual(res_dict[6]['title'], "Step 3-1")
        self.assertEqual(res_dict[7]['title'], "Step 3-2")

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "2")
        self.assertEqual(res_dict[4]['number'], "3")
        self.assertEqual(res_dict[5]['number'], "3-1")
        self.assertEqual(res_dict[6]['number'], "3-2")
        self.assertEqual(res_dict[7]['number'], "3-3")        

        ## copy another step

        res_dict = self.copy_element(base_url=execution_url,
            elem_id=step_id_1_2, insert_after_id=step_id_3_1, level='SIBLING',
            code_expected=200)
        
        logger.debug('copy_element res: %s', json.dumps(res_dict, indent=4))            
        
        self.assertEqual(len(res_dict['numbers']), 2)
        self.assertEqual(res_dict['numbers'][0]['number'], "3-3")
        self.assertEqual(res_dict['numbers'][1]['number'], "3-4")

        self.assertEqual(len(res_dict['elements']), 1)
        self.assertEqual(res_dict['elements'][0]['title'], 'Step 1-2')
        self.assertEqual(res_dict['elements'][0]['number'], '3-3')

        res_dict = self.get_as_run(execution_id)
        logger.debug('copy step as run after res_dict= %s', json.dumps(res_dict, indent=4))            

        res_dict = self.get_elements(execution_url)
        logger.debug('copied step elements res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 9)
        self.assertEqual(res_dict[0]['title'], "Section 1")
        self.assertEqual(res_dict[1]['title'], "Step 1-1")
        self.assertEqual(res_dict[2]['title'], "Step 1-2")
        self.assertEqual(res_dict[3]['title'], 'Paragraph Section 1')
        self.assertEqual(res_dict[4]['title'], "Section 3")
        self.assertEqual(res_dict[5]['title'], "Step 1-1")        
        self.assertEqual(res_dict[6]['title'], "Step 3-1")
        self.assertEqual(res_dict[7]['title'], "Step 1-2")        
        self.assertEqual(res_dict[8]['title'], "Step 3-2")

        self.assertEqual(res_dict[0]['number'], "1")
        self.assertEqual(res_dict[1]['number'], "1-1")
        self.assertEqual(res_dict[2]['number'], "1-2")
        self.assertEqual(res_dict[3]['number'], "2")
        self.assertEqual(res_dict[4]['number'], "3")
        self.assertEqual(res_dict[5]['number'], "3-1")
        self.assertEqual(res_dict[6]['number'], "3-2")
        self.assertEqual(res_dict[7]['number'], "3-3")   
        self.assertEqual(res_dict[8]['number'], "3-4")         

    def test_delete_execution_error(self):
        res_dict = self.delete_execution('not an id', 400)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

    def test_procedure_sections(self):

        rand = random_string()
        title = 'title_' + rand
        procedure_dict = self.create_procedure(title, 'Test procedure', '', 'hongmank')
        procedure_id_1 = procedure_dict['procedure_id']

        rand = random_string()
        description = 'description_' + rand
        version_dict_1 = self.create_procedure_version(procedure_id_1, description, 'hongmank')
        self.assertEqual(version_dict_1['version'], 1)

        rand = random_string()
        title = 'title_' + rand
        procedure_dict = self.create_procedure(title, 'Test procedure', '', 'hongmank')
        procedure_id_2 = procedure_dict['procedure_id']

        rand = random_string()
        description = 'description_' + rand
        version_dict_2 = self.create_procedure_version(procedure_id_2, description, 'hongmank')
        self.assertEqual(version_dict_2['version'], 1)

        description4 = 'My execution is dope'
        venue_id, venue_name = self.create_venue2()
        execution_dict = self.create_execution(venue_id, description4)
        execution_id = execution_dict['execution_id']
        execution_url = shared_dict['host'] + '/executions/' + execution_id

        procedure_section_data_1 = {"reference_procedure_id" : procedure_id_1, "reference_procedure_version" : version_dict_1['version'], 'elem_type': 'PROCEDURE_SECTION',
                                    'title': 'ProcedureSection 1'}
        res = self.add_procedure_section(base_url=execution_url,
            insert_after_id="-1",
            level='CHILD',
            procedure_section=procedure_section_data_1)

        procedure_section_1_id = res['elem']['elem_id']
        procedure_section_1 = self.get_procedure_section(execution_url, procedure_section_1_id)

        self.assertEqual(procedure_section_1['title'], procedure_section_data_1['title'])


        procedure_section_data_2 = {"reference_procedure_id" : procedure_id_2, 
            "reference_procedure_version" : version_dict_2['version'], 
            'elem_type': 'PROCEDURE_SECTION', 
            'description': "this is a description", 
            'title': 'this is a section title'
        }
        res = self.add_procedure_section(base_url=execution_url,
            insert_after_id=procedure_section_1_id,
            level='SIBLING',
            procedure_section=procedure_section_data_2)

        execution_url = shared_dict['host'] + '/executions/' + execution_id
        procedure_sections = self.get_procedure_sections(execution_url)
        self.assertEqual(len(procedure_sections), 2)


        procedure_section_update = {'description': "this is a NEW description"}
        self.update_procedure_section(execution_url, procedure_section_1_id, procedure_section_update)

        procedure_section_1 = self.get_procedure_section(execution_url, procedure_section_1_id)
        self.assertEqual(procedure_section_1['title'], procedure_section_data_1['title'])
        self.assertEqual(procedure_section_1['description'], procedure_section_update['description'])

        self.delete_element(execution_url, procedure_section_1_id, code_expected=200)

        procedure_sections = self.get_procedure_sections(execution_url)
        self.assertEqual(len(procedure_sections), 1)

    def test_procedure_section(self):

        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            title='Section 1')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='SIBLING',
            title='Section 2')

        section_2 = res['elem']
        section_2_id = section_2['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Paragraph 1-1')

        paragraph_1_1 = res['elem']
        paragraph_1_1_id = paragraph_1_1['elem_id']

        # add steps to section 1
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=paragraph_1_1_id,
            level='SIBLING',
            title='Step 1-2')
        logger.debug('res= %s', json.dumps(res, indent=4))

        step_1_2 = res['elem']
        step_1_2_id = step_1_2['elem_id']

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

        #
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=step_1_2_id,
            level='SIBLING',
            title='Step 1-3')

        step_1_3 = res['elem']
        step_1_3_id = step_1_3['elem_id']

        # add steps to section 2
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=section_2_id,
            level='CHILD',
            title='Step 2-1')

        step_2_1 = res['elem']
        step_2_1_id = step_2_1['elem_id']

        #
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=step_2_1_id,
            level='SIBLING',
            title='Step 2-2')

        step_2_2 = res['elem']
        step_2_2_id = step_2_2['elem_id']

        # add version 1
        version_dict = self.create_procedure_version(procedure_id, 'First version', 'hongmank')
        version = version_dict['version']
        self.assertEqual(version, 1)

        # check structure
        procedure_dict = self.get_version_structure(procedure_id, version)
        logger.debug('procedure_dict= %s', json.dumps(procedure_dict, indent=4))

        self.assertEqual(procedure_dict['children'][0]['children'][1]['title'], 'Step 1-2')
        self.assertEqual(procedure_dict['children'][0]['children'][1]['authoring_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(procedure_dict['children'][0]['children'][1].get('execution_user_input'), {})
        
        # add a comment to a step
        procedure_version_url = '{0}/versions/1'.format(procedure_url)
        version_1_step_1_2_id = procedure_dict['children'][0]['children'][1]['elem_id']
        res_dict = self.add_conversation(procedure_version_url, version_1_step_1_2_id, {'type': 'COMMENT'})     
        conversation_id = res_dict['conversation_id']
        comment = res_dict['comments'][0]
        comment_id = comment['comment_id']          
        
        content = 'This is the first comment for the step'        
        res_dict = self.update_comment(procedure_version_url, version_1_step_1_2_id, conversation_id, comment_id, content)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['content'], content)    

        #####
        execution_description = 'Execution with procedure section'
        venue_id, venue_name = self.create_venue2()
        execution_dict = self.create_execution(venue_id, execution_description)
        execution_id = execution_dict['execution_id']
        execution_url = shared_dict['host'] + '/executions/' + execution_id

        procedure_section_data = {'elem_type': 'PROCEDURE_SECTION',
                                    'title': 'Procedure Section 1'}
        res = self.add_procedure_section(base_url=execution_url,
            insert_after_id="-1",
            level='CHILD',
            procedure_section=procedure_section_data)

        procedure_section_id = res['elem']['elem_id']
        procedure_section = self.get_procedure_section(execution_url, procedure_section_id)
        self.assertEqual(procedure_section['title'], procedure_section_data['title'])

        outline_elems = self.get_outline(procedure_url, version)
        self.assertEquals(len(outline_elems), 7)
        self.assertEquals(outline_elems[0]['parent_id'], '')
        self.assertEquals(outline_elems[1]['parent_id'], outline_elems[0]['elem_id'])

        procedure_section_input = {
            'reference_procedure_id': procedure_id,
            'reference_procedure_version': version,
            'elements': outline_elems,
            'reference_procedure_version_description': '',
            'reference_procedure_title': '',
            'run_for_score': False
        }

        self.update_procedure_section_input(execution_url, procedure_section_id, procedure_section_input)

        user_input = self.get_procedure_section_input(execution_url, procedure_section_id)

        self.assertDictEqual(procedure_section_input, user_input)

        proc_section_elems = self.import_procedure_section(execution_id, procedure_section_id)
        logger.debug('proc_section_elems= %s', json.dumps(proc_section_elems, indent=4))
        for proc_section_elem in proc_section_elems:
            self.assertEqual(len(proc_section_elem['conversations']), 0)

        self.assertEqual(proc_section_elems[3]['title'], 'Step 1-2')
        self.assertEqual(proc_section_elems[3]['number'], '1-2')
        self.assertEqual(proc_section_elems[3]['authoring_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(proc_section_elems[3]['execution_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(proc_section_elems[7]['title'], 'Step 2-2')
        self.assertEqual(proc_section_elems[7]['number'], '2-2')

        as_run_dict = self.get_as_run(execution_id)
        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))
        self.assertEqual(as_run_dict['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['elem_type'], 'PROCEDURE_SECTION')
        self.assertEqual(as_run_dict['children'][0]['run_for_score'], False)
        self.assertEqual(as_run_dict['children'][0]['execution_user_input']['run_for_score'], False)        
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['title'], 'Step 1-2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['number'], '1-2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['authoring_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['execution_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['title'], 'Step 2-2')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['number'], '2-2')

        # add a paragraph to procedure section
        proc_section_secion_1_id = as_run_dict['children'][0]['children'][0]['elem_id']
        logger.debug('proc_section_secion_1_id= %s', proc_section_secion_1_id)

        proc_section_step_1_2_id = as_run_dict['children'][0]['children'][0]['children'][1]['elem_id']
        logger.debug('proc_section_step_1_2_id= %s', proc_section_step_1_2_id)

        res = self.add_paragraph(base_url=execution_url,
            insert_after_id=proc_section_step_1_2_id,
            level='SIBLING',
            title='Paragraph 1-2.1 in Procedure Section')
        logger.debug('res= %s', json.dumps(res, indent=4))

        as_run_dict = self.get_as_run(execution_id)
        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))        

        proc_section_paragraph_1_2__1 = res['elem']
        numbers = res['numbers']
        proc_section_paragraph_1_2__1_id = proc_section_paragraph_1_2__1['elem_id']

        self.assertEqual(len(numbers), 1)
        self.assertEqual(proc_section_paragraph_1_2__1['number'], '1-2.1')        

        # add steps to procedure section
        res = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=proc_section_paragraph_1_2__1_id,
            level='SIBLING',
            title='Step 1-2.3')
        logger.debug('res= %s', json.dumps(res, indent=4))

        step_1_2__3 = res['elem']
        numbers = res['numbers']
        self.assertEqual(len(numbers), 1)
        self.assertEqual(step_1_2__3['number'], '1-2.2')
        step_1_2__3_id = step_1_2__3['elem_id']

        res = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=proc_section_paragraph_1_2__1_id,
            level='SIBLING',
            title='Step 1-2.2')
        logger.debug('res= %s', json.dumps(res, indent=4))

        step_1_2__2 = res['elem']
        numbers = res['numbers']
        self.assertEqual(len(numbers), 2)
        self.assertEqual(step_1_2__2['number'], '1-2.2')
        step_1_2__2_id = step_1_2__2['elem_id']

        #
        as_run_dict = self.get_as_run(execution_id)
        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))

        self.assertEqual(as_run_dict['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['elem_type'], 'PROCEDURE_SECTION')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['elem_type'], 'SECTION')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['title'], 'Section 1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['number'], '1-1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['title'], 'Paragraph 1-1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['number'], '1-2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['title'], 'Step 1-2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['number'], '1-2.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['title'], 'Paragraph 1-2.1 in Procedure Section')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['number'], '1-2.2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['title'], 'Step 1-2.2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['number'], '1-2.3')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['title'], 'Step 1-2.3')

        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['number'], '2-2')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['title'], 'Step 2-2')

        # add step as the first element of a section
        res = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=proc_section_secion_1_id,
            level='CHILD',
            title='Step 1-0.1')
        logger.debug('res Step 1-0.1= %s', json.dumps(res, indent=4))

        step_1_0__1 = res['elem']
        numbers = res['numbers']
        self.assertEqual(len(numbers), 1)
        self.assertEqual(step_1_0__1['number'], '1-0.1')
        step_1_0__1_id = step_1_0__1['elem_id']

        as_run_dict = self.get_as_run(execution_id)
        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))
        self.assertEqual(as_run_dict['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['elem_type'], 'PROCEDURE_SECTION')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['elem_type'], 'SECTION')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['title'], 'Section 1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['number'], '1-0.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['title'], 'Step 1-0.1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['number'], "1-1")
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['title'], 'Paragraph 1-1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['number'], '1-2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['title'], 'Step 1-2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['number'], '1-2.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['title'], 'Paragraph 1-2.1 in Procedure Section')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['number'], '1-2.2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['title'], 'Step 1-2.2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['number'], '1-2.3')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['title'], 'Step 1-2.3')

        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['number'], '2-2')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['title'], 'Step 2-2')

        # add a section
        res = self.add_section(base_url=execution_url,
            insert_after_id=proc_section_step_1_2_id,
            level='SIBLING',
            title='Section 1-2.1')

        logger.debug('res Section 1-2.1= %s', json.dumps(res, indent=4))
        proc_section_section_1_2__1_id = res['elem']['elem_id']
        self.assertEqual(len(res['numbers']), 4)

        as_run_dict = self.get_as_run(execution_id)
        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))
        self.assertEqual(as_run_dict['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['elem_type'], 'PROCEDURE_SECTION')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['elem_type'], 'SECTION')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['title'], 'Section 1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['number'], '1-0.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['title'], 'Step 1-0.1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['number'], '1-1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['title'], 'Paragraph 1-1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['number'], '1-2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['title'], 'Step 1-2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['number'], '1-2.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['elem_type'], 'SECTION')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['title'], 'Section 1-2.1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['number'], '1-2.2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['title'], 'Paragraph 1-2.1 in Procedure Section')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['number'], '1-2.3')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['title'], 'Step 1-2.2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][6]['number'], '1-2.4')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][6]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][6]['title'], 'Step 1-2.3')

        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['number'], '2-2')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['title'], 'Step 2-2')

        # add steps to the section
        res = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=proc_section_section_1_2__1_id,
            level='CHILD',
            title='Step 1-2.1.1')
        logger.debug('res Step 1-2.1.1= %s', json.dumps(res, indent=4))
        proc_section_step_1_2__1__1_id = res['elem']['elem_id']
        self.assertEqual(len(res['numbers']), 1)
        self.assertEqual(res['numbers'][0]['elem_id'], proc_section_step_1_2__1__1_id)

        res = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=proc_section_step_1_2__1__1_id,
            level='SIBLING',
            title='Step 1-2.1.2')
        logger.debug('res Step 1-2.1.2= %s', json.dumps(res, indent=4))
        proc_section_step_1_2__1__2_id = res['elem']['elem_id']
        self.assertEqual(len(res['numbers']), 1)
        self.assertEqual(res['numbers'][0]['elem_id'], proc_section_step_1_2__1__2_id)

        as_run_dict = self.get_as_run(execution_id)
        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))
        self.assertEqual(as_run_dict['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['elem_type'], 'PROCEDURE_SECTION')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['elem_type'], 'SECTION')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['title'], 'Section 1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['number'], '1-0.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['title'], 'Step 1-0.1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['number'], '1-1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['title'], 'Paragraph 1-1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['number'], '1-2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['title'], 'Step 1-2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['number'], '1-2.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['elem_type'], 'SECTION')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['title'], 'Section 1-2.1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['children'][0]['number'], '1-2.1.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['children'][0]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['children'][0]['title'], 'Step 1-2.1.1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['children'][1]['number'], '1-2.1.2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['children'][1]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['children'][1]['title'], 'Step 1-2.1.2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['number'], '1-2.2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['title'], 'Paragraph 1-2.1 in Procedure Section')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['number'], '1-2.3')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['title'], 'Step 1-2.2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][6]['number'], '1-2.4')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][6]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][6]['title'], 'Step 1-2.3')

        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['number'], '2-2')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['title'], 'Step 2-2')


        # delete section
        res = self.delete_element(execution_url, proc_section_section_1_2__1_id)

        logger.debug('res delete Section 1-1.1= %s', json.dumps(res, indent=4))

        self.assertEqual(len(res['numbers']), 3)

        as_run_dict = self.get_as_run(execution_id)
        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))
        self.assertEqual(as_run_dict['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['elem_type'], 'PROCEDURE_SECTION')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['elem_type'], 'SECTION')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['title'], 'Section 1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['number'], '1-0.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][0]['title'], 'Step 1-0.1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['number'], '1-1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['title'], 'Paragraph 1-1')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['number'], '1-2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][2]['title'], 'Step 1-2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['number'], '1-2.1')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['elem_type'], 'PARAGRAPH')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][3]['title'], 'Paragraph 1-2.1 in Procedure Section')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['number'], '1-2.2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][4]['title'], 'Step 1-2.2')

        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['number'], '1-2.3')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][5]['title'], 'Step 1-2.3')

        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['number'], '2-2')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['elem_type'], 'STEP')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['title'], 'Step 2-2')

        ### now add more elements and create version 2
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,
            insert_after_id=step_2_2_id,
            level='SIBLING',
            title='Step 2-3')

        step_2_3 = res['elem']
        step_2_3_id = step_2_2['elem_id']

        # add version 2
        version_dict = self.create_procedure_version(procedure_id, 'Second version', 'hongmank')
        version = version_dict['version']
        self.assertEqual(version, 2)

        # update procedure section
        outline_elems = self.get_outline(procedure_url, version)

        procedure_section_input = {
            'reference_procedure_id': procedure_id,
            'reference_procedure_version': version,
            'elements': outline_elems,
            'reference_procedure_version_description': '',
            'reference_procedure_title': '',
            'run_for_score': False
        }

        self.update_procedure_section_input(execution_url, procedure_section_id, procedure_section_input)

        # Cannot import procedure again
        proc_section_elems = self.import_procedure_section(execution_id, procedure_section_id, 400)

        # Add another procedure section
        procedure_section_data_2 = {'elem_type': 'PROCEDURE_SECTION',
                                    'title': 'Procedure Section 2'}
        res = self.add_procedure_section(base_url=execution_url,
            insert_after_id=procedure_section_id,
            level='SIBLING',
            procedure_section=procedure_section_data_2)

        procedure_section_id_2 = res['elem']['elem_id']
        procedure_section_2 = self.get_procedure_section(execution_url, procedure_section_id_2)
        logger.debug('procedure_section_2= %s', json.dumps(procedure_section_2, indent=4))


        ### create another procedure and version
        rand_2 = random_string()
        title_2 = 'title_' + rand_2
        procedure_dict = self.create_procedure(title_2, 'Test procedure 2', '', 'hongmank')

        procedure_id_2 = procedure_dict['procedure_id']
        procedure_url_2 = shared_dict['host'] + '/procedures/' + procedure_id_2

        # Add section
        res = self.add_section(base_url=procedure_url_2,
            insert_after_id=-1,
            level='CHILD',
            title='Section 1 New')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        # add steps to section 1
        res = self.add_step_generic(base_url=procedure_url_2,
            step_type=StepTypes.ENVIRONMENT_MANUAL,        
            insert_after_id=section_1_id,
            level='CHILD',
            title='Step 1-1 New')

        step_1_1 = res['elem']
        step_1_1_id = step_1_1['elem_id']

        # add version 1
        version_dict = self.create_procedure_version(procedure_id_2, 'First version', 'hongmank')
        version = version_dict['version']
        self.assertEqual(version, 1)

        # update procedure section using procedure 2
        outline_elems = self.get_outline(procedure_url_2, version)

        procedure_section_input = {
            'reference_procedure_id': procedure_id_2,
            'reference_procedure_version': version,
            'elements': outline_elems,
            'reference_procedure_version_description': '',
            'reference_procedure_title': '',
            'run_for_score': False            
        }

        self.update_procedure_section_input(execution_url, procedure_section_id_2, procedure_section_input)


        logger.debug('import procedure 2')
        proc_section_elems = self.import_procedure_section(execution_id, procedure_section_id_2)
        logger.debug('proc_section_elems= %s', json.dumps(proc_section_elems, indent=4))

        self.assertEqual(proc_section_elems[2]['title'], 'Step 1-1 New')
        self.assertEqual(proc_section_elems[2]['number'], '1-1')


        as_run_dict = self.get_as_run(execution_id)
        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))
        self.assertEqual(as_run_dict['children'][1]['number'], '2')
        self.assertEqual(as_run_dict['children'][1]['elem_type'], 'PROCEDURE_SECTION')
        self.assertEqual(len(as_run_dict['children'][1]['children'][0]['children']), 1)
        self.assertEqual(as_run_dict['children'][1]['children'][0]['children'][0]['title'], 'Step 1-1 New')
        self.assertEqual(as_run_dict['children'][1]['children'][0]['children'][0]['number'], '1-1')

        # get structure of selected elems
        outline_elems = self.get_outline(procedure_url, version)
        logger.debug('outline_elems= %s', json.dumps(outline_elems, indent=4))

        # Add another procedure section
        procedure_section_data_3 = {'elem_type': 'PROCEDURE_SECTION',
                                    'title': 'Procedure Section 3'}
        res = self.add_procedure_section(base_url=execution_url,
            insert_after_id=procedure_section_id_2,
            level='SIBLING',
            procedure_section=procedure_section_data_3)

        procedure_section_id_3 = res['elem']['elem_id']
        procedure_section_3 = self.get_procedure_section(execution_url, procedure_section_id_3)
        logger.debug('procedure_section_3= %s', json.dumps(procedure_section_3, indent=4))


        procedure_section_input = {
            'reference_procedure_id': procedure_id,
            'reference_procedure_version': version,
            'elements': outline_elems,
            'reference_procedure_version_description': '',
            'reference_procedure_title': '',
            'run_for_score': False             
        }

        self.update_procedure_section_input(execution_url, procedure_section_id_3, procedure_section_input)
        procedure_section_structure = self.get_procedure_section_structure(base_url=execution_url, elem_id=procedure_section_id_3, code_expected=200)
        logger.debug('all procedure_section_structure= %s', json.dumps(procedure_section_structure, indent=4))
        self.assertEqual(len(procedure_section_structure['children']), 2)
        self.assertEqual(procedure_section_structure['children'][0]['title'], 'Section 1')
        self.assertEqual(procedure_section_structure['children'][1]['title'], 'Section 2')

        procedure_section_elements = self.get_procedure_section_elements(base_url=execution_url, elem_id=procedure_section_id_3, code_expected=200)
        logger.debug('all procedure_section_elements= %s', json.dumps(procedure_section_elements, indent=4))
        self.assertEqual(len(procedure_section_elements), 7)
        self.assertEqual(procedure_section_elements[0]['title'], 'Section 1')
        self.assertEqual(procedure_section_elements[4]['title'], 'Section 2')        

        outline_elems[0]['selected'] = False
        self.update_procedure_section_input(execution_url, procedure_section_id_3, procedure_section_input)
        procedure_section_structure = self.get_procedure_section_structure(base_url=execution_url, elem_id=procedure_section_id_3, code_expected=200)
        logger.debug('selected procedure_section_structure= %s', json.dumps(procedure_section_structure, indent=4))
        self.assertEqual(len(procedure_section_structure['children']), 1)
        self.assertEqual(procedure_section_structure['children'][0]['title'], 'Section 2')

        procedure_section_elements = self.get_procedure_section_elements(base_url=execution_url, elem_id=procedure_section_id_3, code_expected=200)
        logger.debug('selected procedure_section_elements= %s', json.dumps(procedure_section_elements, indent=4))
        self.assertEqual(len(procedure_section_elements), 3)
        self.assertEqual(procedure_section_elements[0]['title'], 'Section 2')       

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))   
        
                
        # copy procedure section
        res_dict = self.copy_element(execution_url, procedure_section_id_3, procedure_section_id_3, 'SIBLING', 200) 
        logger.debug('copy_element res_dict= %s', json.dumps(res_dict, indent=4))   
        self.assertEqual(len(res_dict['elements']), 1)     
        self.assertEqual(res_dict['elements'][0]['elem_type'], 'PROCEDURE_SECTION') 
        self.assertEqual(res_dict['elements'][0]['number'], '4')       
        self.assertEqual(len(res_dict['elem_ids']), 17)           

    def test_procedure_section_nested(self):

        rand_1 = random_string()
        title_1 = 'title_' + rand_1
        procedure_dict_1 = self.create_procedure(title_1, 'Test procedure', '', 'hongmank')

        procedure_id_1 = procedure_dict_1['procedure_id']
        procedure_url_1 = shared_dict['host'] + '/procedures/' + procedure_id_1

        # Add section
        res = self.add_section(base_url=procedure_url_1,
            insert_after_id=-1,
            level='CHILD',
            title='Section 1')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        res = self.add_section(base_url=procedure_url_1,
            insert_after_id=section_1_id,
            level='SIBLING',
            title='Section 2')

        section_2 = res['elem']
        section_2_id = section_2['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url_1,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Paragraph A')

        paragraph_a = res['elem']
        paragraph_a_id = paragraph_a['elem_id']

        # add steps to section 1
        res = self.add_step_generic(base_url=procedure_url_1,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=paragraph_a_id,
            level='SIBLING',
            title='Step 1-1')
        logger.debug('res= %s', json.dumps(res, indent=4))

        step_1_1 = res['elem']
        step_1_1_id = step_1_1['elem_id']

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
        self.set_step_input_generic(procedure_url_1, step_1_1_id, authoring_user_input)

        #
        res = self.add_step_generic(base_url=procedure_url_1,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=step_1_1_id,
            level='SIBLING',
            title='Step 1-2')

        step_1_2 = res['elem']
        step_1_2_id = step_1_2['elem_id']

        # add steps to section 2
        res = self.add_step_generic(base_url=procedure_url_1,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=section_2_id,
            level='CHILD',
            title='Step 2-1')

        step_2_1 = res['elem']
        step_2_1_id = step_2_1['elem_id']

        #
        res = self.add_step_generic(base_url=procedure_url_1,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=step_2_1_id,
            level='SIBLING',
            title='Step 2-2')

        step_2_2 = res['elem']
        step_2_2_id = step_2_2['elem_id']

        # add version 1
        version_dict = self.create_procedure_version(procedure_id_1, 'First version', 'hongmank')
        version = version_dict['version']
        self.assertEqual(version, 1)

        ### create parent procedure
        rand_2 = random_string()
        title_2 = 'title_' + rand_2
        procedure_dict_2 = self.create_procedure(title_1, 'Parent procedure', '', 'hongmank')

        procedure_id_2 = procedure_dict_2['procedure_id']
        procedure_url_2 = shared_dict['host'] + '/procedures/' + procedure_id_2

        # Add procedure section to procedure
        version = 1
        procedure_section_data_2 = {"reference_procedure_id" : procedure_id_1, "reference_procedure_version" : version, 'elem_type': 'PROCEDURE_SECTION',
                                    'title': 'ProcedureSection 1'}

        res = self.add_procedure_section(base_url=procedure_url_2,
            insert_after_id="-1",
            level='CHILD',
            procedure_section=procedure_section_data_2)

        procedure_section_2 = res['elem']
        procedure_section_id_2 = procedure_section_2['elem_id']

        # check structure
        outline_elems = self.get_outline(procedure_url_1, version)
        logger.debug('outline_elems= %s', json.dumps(outline_elems, indent=4))

        procedure_section_input = {
            'reference_procedure_id': procedure_id_1,
            'reference_procedure_version': version,
            'elements': outline_elems,
            'reference_procedure_version_description': '',
            'reference_procedure_title': '',
            'run_for_score': False            
        }

        self.update_procedure_section_input(procedure_url_2, procedure_section_id_2, procedure_section_input)
        procedure_section_structure = self.get_procedure_section_structure(base_url=procedure_url_2, elem_id=procedure_section_id_2)
        logger.debug('all procedure_section_structure= %s', json.dumps(procedure_section_structure, indent=4))
        self.assertEqual(len(procedure_section_structure['children']), 2)
        self.assertEqual(procedure_section_structure['children'][0]['title'], 'Section 1')
        self.assertEqual(procedure_section_structure['children'][1]['title'], 'Section 2')

        procedure_section_elements = self.get_procedure_section_elements(base_url=procedure_url_2, elem_id=procedure_section_id_2)
        logger.debug('all procedure_section_elements= %s', json.dumps(procedure_section_elements, indent=4))
        self.assertEqual(len(procedure_section_elements), 7)
        self.assertEqual(procedure_section_elements[0]['title'], 'Section 1')
        self.assertEqual(procedure_section_elements[4]['title'], 'Section 2')        

        outline_elems[0]['selected'] = False
        self.update_procedure_section_input(procedure_url_2, procedure_section_id_2, procedure_section_input)
        procedure_section_structure = self.get_procedure_section_structure(base_url=procedure_url_2, elem_id=procedure_section_id_2)
        logger.debug('selected procedure_section_structure= %s', json.dumps(procedure_section_structure, indent=4))
        self.assertEqual(len(procedure_section_structure['children']), 1)
        self.assertEqual(procedure_section_structure['children'][0]['title'], 'Section 2')

        procedure_section_elements = self.get_procedure_section_elements(base_url=procedure_url_2, elem_id=procedure_section_id_2)
        logger.debug('selected procedure_section_elements= %s', json.dumps(procedure_section_elements, indent=4))
        self.assertEqual(len(procedure_section_elements), 3)
        self.assertEqual(procedure_section_elements[0]['title'], 'Section 2')      

    def test_execution_boundary(self):
        self.create_execution_example()
        
        id_dict = self.create_execution_example()
        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        paragraph_id_2 = id_dict['paragraph_id_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        self.update_execution(execution_id, 
            {'mode': 'AUTO', 'pause_conditions': {'on_fail': False, 'on_error': False, 'on_section_end': True, 'on_procedure_end': False}}, 
            code_expected=200)

        execution = self.set_boundary_element(execution_url, section_id_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], paragraph_id_2)

        execution = self.set_boundary_element(execution_url, step_id_1_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], paragraph_id_2)

        execution = self.set_boundary_element(execution_url, step_id_1_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], paragraph_id_2)        

        execution = self.set_boundary_element(execution_url, paragraph_id_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], '')  

        execution = self.set_boundary_element(execution_url, section_id_3)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], '')    

        execution = self.set_boundary_element(execution_url, step_id_3_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], '')  

        execution = self.set_boundary_element(execution_url, step_id_3_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], '')                   

        ### Add a procedure section

        id_dict = self.create_procedure_example()
        procedure_id = id_dict['procedure_id']
        procedure_url = id_dict['procedure_url']
        procedure_title = id_dict['procedure_title']
        version = id_dict['version']
        version_description = id_dict['version_description']

        procedure_section_data = {'elem_type': 'PROCEDURE_SECTION',
                                    'title': 'Procedure Section 4'}
        res = self.add_procedure_section(base_url=execution_url,
            insert_after_id=section_id_3,
            level='SIBLING',
            procedure_section=procedure_section_data)

        procedure_section_id = res['elem']['elem_id']
        procedure_section = self.get_procedure_section(execution_url, procedure_section_id)
        outline_elems = self.get_outline(procedure_url, version)

        procedure_section_input = {
            'reference_procedure_id': procedure_id,
            'reference_procedure_version': version,
            'elements': outline_elems,
            'reference_procedure_version_description': version_description,
            'reference_procedure_title': procedure_title,
            'run_for_score': True
        }

        self.update_procedure_section_input(execution_url, procedure_section_id, procedure_section_input)
        proc_section_elems = self.import_procedure_section(execution_id, procedure_section_id)
        logger.debug('proc_section_elems= %s', json.dumps(proc_section_elems, indent=4))

        proc_section_id_1 = proc_section_elems[1]['elem_id']
        proc_paragraph_id_1_1 = proc_section_elems[2]['elem_id']
        proc_step_id_1_2 = proc_section_elems[3]['elem_id']
        proc_step_id_1_3 = proc_section_elems[4]['elem_id']
        proc_section_id_2 = proc_section_elems[5]['elem_id']
        proc_step_id_2_1 = proc_section_elems[6]['elem_id']       
        proc_step_id_2_2 = proc_section_elems[7]['elem_id']          

        #
        res = self.add_section(base_url=execution_url,
            insert_after_id=procedure_section_id,
            level='SIBLING',
            title='Section 5')        

        logger.debug('res= %s', json.dumps(res, indent=4))

        section_id_5 = res['elem']['elem_id']       

        execution = self.set_boundary_element(execution_url, proc_section_id_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], proc_section_id_2)   

        execution = self.set_boundary_element(execution_url, proc_paragraph_id_1_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], proc_section_id_2)       

        execution = self.set_boundary_element(execution_url, proc_step_id_1_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], proc_section_id_2)         

        execution = self.set_boundary_element(execution_url, proc_step_id_1_3)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], proc_section_id_2)  

        execution = self.set_boundary_element(execution_url, proc_section_id_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)            

        execution = self.set_boundary_element(execution_url, proc_step_id_2_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)        

        execution = self.set_boundary_element(execution_url, proc_step_id_2_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)                     

        ### If on_section_end and on_procedure_end are true, on_section_end takes precedence
        self.update_execution(execution_id, 
            {'mode': 'AUTO', 'pause_conditions': {'on_fail': False, 'on_error': False, 'on_section_end': True, 'on_procedure_end': True}}, 
            code_expected=200)          

        execution = self.set_boundary_element(execution_url, proc_section_id_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], proc_section_id_2)   

        execution = self.set_boundary_element(execution_url, proc_paragraph_id_1_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], proc_section_id_2)       

        execution = self.set_boundary_element(execution_url, proc_step_id_1_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], proc_section_id_2)         

        execution = self.set_boundary_element(execution_url, proc_step_id_1_3)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], proc_section_id_2)  

        execution = self.set_boundary_element(execution_url, proc_section_id_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)            

        execution = self.set_boundary_element(execution_url, proc_step_id_2_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)        

        execution = self.set_boundary_element(execution_url, proc_step_id_2_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)         

        ### on_procedure_end
        self.update_execution(execution_id, 
            {'mode': 'AUTO', 'pause_conditions': {'on_fail': False, 'on_error': False, 'on_section_end': False, 'on_procedure_end': True}}, 
            code_expected=200)          

        execution = self.set_boundary_element(execution_url, proc_section_id_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)   

        execution = self.set_boundary_element(execution_url, proc_paragraph_id_1_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)       

        execution = self.set_boundary_element(execution_url, proc_step_id_1_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)         

        execution = self.set_boundary_element(execution_url, proc_step_id_1_3)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)  

        execution = self.set_boundary_element(execution_url, proc_section_id_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)            

        execution = self.set_boundary_element(execution_url, proc_step_id_2_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)        

        execution = self.set_boundary_element(execution_url, proc_step_id_2_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], section_id_5)             

        ### on_procedure_end for an element that is not in a procedure
        execution = self.set_boundary_element(execution_url, section_id_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], procedure_section_id)  

        execution = self.set_boundary_element(execution_url, step_id_1_1)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], procedure_section_id) 

        execution = self.set_boundary_element(execution_url, step_id_1_2)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], procedure_section_id) 

        execution = self.set_boundary_element(execution_url, section_id_5)
        logger.debug('execution= %s', json.dumps(execution, indent=4))
        self.assertEqual(execution['boundary_elem_id'], '')                           

    def create_procedure_example(self):  

        id_dict = {}

        rand_1 = random_string()
        procedure_title = 'title_' + rand_1
        procedure_dict = self.create_procedure(procedure_title, 'Test procedure', '', 'hongmank')

        procedure_id = procedure_dict['procedure_id']
        procedure_url = shared_dict['host'] + '/procedures/' + procedure_id

        # Add section
        res = self.add_section(base_url=procedure_url,
            insert_after_id=-1,
            level='CHILD',
            title='Section 1')

        section_1 = res['elem']
        section_1_id = section_1['elem_id']

        res = self.add_section(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='SIBLING',
            title='Section 2')

        section_2 = res['elem']
        section_2_id = section_2['elem_id']

        # add paragraph
        res = self.add_paragraph(base_url=procedure_url,
            insert_after_id=section_1_id,
            level='CHILD',
            title='Paragraph 1-1')

        paragraph_1_1 = res['elem']
        paragraph_1_1_id = paragraph_1_1['elem_id']

        # add steps to section 1
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=paragraph_1_1_id,
            level='SIBLING',
            title='Step 1-2')
        logger.debug('res= %s', json.dumps(res, indent=4))

        step_1_2 = res['elem']
        step_1_2_id = step_1_2['elem_id']

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

        #
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=step_1_2_id,
            level='SIBLING',
            title='Step 1-3')

        step_1_3 = res['elem']
        step_1_3_id = step_1_3['elem_id']

        # add steps to section 2
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=section_2_id,
            level='CHILD',
            title='Step 2-1')

        step_2_1 = res['elem']
        step_2_1_id = step_2_1['elem_id']

        #
        res = self.add_step_generic(base_url=procedure_url,
            step_type=StepTypes.ENVIRONMENT_MANUAL,          
            insert_after_id=step_2_1_id,
            level='SIBLING',
            title='Step 2-2')

        step_2_2 = res['elem']
        step_2_2_id = step_2_2['elem_id']

        # add version 1
        version_description = 'First version'
        version_dict = self.create_procedure_version(procedure_id, version_description, 'hongmank')
        version = version_dict['version']
        self.assertEqual(version, 1)

        # check structure
        procedure_dict = self.get_version_structure(procedure_id, version)
        logger.debug('procedure_dict= %s', json.dumps(procedure_dict, indent=4))

        self.assertEqual(procedure_dict['children'][0]['children'][1]['title'], 'Step 1-2')
        self.assertEqual(procedure_dict['children'][0]['children'][1]['authoring_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(procedure_dict['children'][0]['children'][1].get('execution_user_input'), {})

        """
        id_dict = {
            'procedure_url': procedure_url,
            'procedure_title': procedure_title,            
            'procedure_id': procedure_id,
            'version': version,
            'version_description': version_description,
            'section_1_id': procedure_dict['children'][0]['elem_id'],
            'paragraph_1_1_id': procedure_dict['children'][0]['children'][0]['elem_id'],
            'step_1_2_id': procedure_dict['children'][0]['children'][1]['elem_id'],
            'step_1_3_id': procedure_dict['children'][0]['children'][2]['elem_id'],
            'section_2_id': procedure_dict['children'][1]['elem_id'],
            'step_2_1_id': procedure_dict['children'][1]['children'][0]['elem_id'],
            'step_2_2_id': procedure_dict['children'][1]['children'][1]['elem_id']
        }
        """

        # return version 0 so that it can be used as a target of copy
        id_dict = {
            'procedure_url': procedure_url,
            'procedure_title': procedure_title,            
            'procedure_id': procedure_id,
            'version': 0,
            'version_description': version_description,
            'section_1_id': section_1_id,
            'paragraph_1_1_id': paragraph_1_1_id,
            'step_1_2_id': step_1_2_id,
            'step_1_3_id': step_1_3_id,
            'section_2_id': section_2_id,
            'step_2_1_id': step_2_1_id,
            'step_2_2_id': step_2_2_id
        }

        return id_dict      

    def test_redline(self):
        self.create_redline_example(complete=False)

    def test_redline_discard(self):
        self.create_redline_example(complete=True)

    def create_redline_example(self, complete=False):

        id_dict = self.create_procedure_example()
        procedure_id = id_dict['procedure_id']
        procedure_url = id_dict['procedure_url']
        procedure_title = id_dict['procedure_title']
        version = id_dict['version']
        version_description = id_dict['version_description']

        #####
        execution_description = 'Execution with procedure section'
        venue_id, venue_name = self.create_venue2()
        execution_dict = self.create_execution(venue_id, execution_description)
        execution_id = execution_dict['execution_id']
        execution_url = shared_dict['host'] + '/executions/' + execution_id

        procedure_section_data = {'elem_type': 'PROCEDURE_SECTION',
                                    'title': 'Procedure Section 1'}
        res = self.add_procedure_section(base_url=execution_url,
            insert_after_id="-1",
            level='CHILD',
            procedure_section=procedure_section_data)

        procedure_section_id = res['elem']['elem_id']
        procedure_section = self.get_procedure_section(execution_url, procedure_section_id)
        self.assertEqual(procedure_section['title'], procedure_section_data['title'])
        self.assertEqual(procedure_section['run_for_score'], False)
        self.assertEqual(procedure_section['execution_user_input']['run_for_score'], False)        

        outline_elems = self.get_outline(procedure_url, version)
        self.assertEquals(len(outline_elems), 7)
        self.assertEquals(outline_elems[0]['parent_id'], '')
        self.assertEquals(outline_elems[1]['parent_id'], outline_elems[0]['elem_id'])


        procedure_section_input = {
            'reference_procedure_id': procedure_id,
            'reference_procedure_version': version,
            'elements': outline_elems,
            'reference_procedure_version_description': version_description,
            'reference_procedure_title': procedure_title,
            'run_for_score': True
        }

        self.update_procedure_section_input(execution_url, procedure_section_id, procedure_section_input)

        user_input = self.get_procedure_section_input(execution_url, procedure_section_id)

        self.assertDictEqual(procedure_section_input, user_input)

        proc_section_elems = self.import_procedure_section(execution_id, procedure_section_id)
        logger.debug('proc_section_elems= %s', json.dumps(proc_section_elems, indent=4))

        self.assertEqual(proc_section_elems[0]['elem_id'], procedure_section_id)
        self.assertEqual(proc_section_elems[0]['imported'], True)
        self.assertEqual(proc_section_elems[0]['executed'], False)
        self.assertEqual(proc_section_elems[3]['title'], 'Step 1-2')
        self.assertEqual(proc_section_elems[3]['number'], '1-2')
        self.assertEqual(proc_section_elems[3]['authoring_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(proc_section_elems[3]['execution_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(proc_section_elems[3]['run_for_score'], True)
        self.assertEqual(proc_section_elems[7]['title'], 'Step 2-2')
        self.assertEqual(proc_section_elems[7]['number'], '2-2')

        as_run_dict = self.get_as_run(execution_id)

        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))
        self.assertEqual(as_run_dict['children'][0]['number'], '1')
        self.assertEqual(as_run_dict['children'][0]['elem_type'], 'PROCEDURE_SECTION')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['title'], 'Step 1-2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['number'], '1-2')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['authoring_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(as_run_dict['children'][0]['children'][0]['children'][1]['execution_user_input']['temperature']['verification_condition'], 'RECORD')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['title'], 'Step 2-2')
        self.assertEqual(as_run_dict['children'][0]['children'][1]['children'][1]['number'], '2-2')

        proc_section_section_1_id = as_run_dict['children'][0]['children'][0]['elem_id']
        logger.debug('proc_section_secion_1_id= %s', proc_section_section_1_id)

        proc_section_paragraph_1_1_id = as_run_dict['children'][0]['children'][0]['children'][0]['elem_id']
        logger.debug('proc_section_paragraph_1_1_id= %s', proc_section_paragraph_1_1_id)        

        proc_section_step_1_2_id = as_run_dict['children'][0]['children'][0]['children'][1]['elem_id']
        logger.debug('proc_section_step_1_2_id= %s', proc_section_step_1_2_id)

        proc_section_step_1_3_id = as_run_dict['children'][0]['children'][0]['children'][2]['elem_id']
        logger.debug('proc_section_step_1_3_id= %s', proc_section_step_1_3_id)        

        proc_section_secion_2_id = as_run_dict['children'][0]['children'][1]['elem_id']
        logger.debug('proc_section_secion_2_id= %s', proc_section_secion_2_id)     

        proc_section_step_2_1_id = as_run_dict['children'][0]['children'][1]['children'][0]['elem_id']
        logger.debug('proc_section_step_2_1_id= %s', proc_section_step_2_1_id)        

        proc_section_step_2_2_id = as_run_dict['children'][0]['children'][1]['children'][1]['elem_id']
        logger.debug('proc_section_step_2_2_id= %s', proc_section_step_2_2_id)           

        modify_res = self.modify_element(execution_id, proc_section_step_2_1_id)
        # create a redline by modification
        logger.debug('modify_res= %s', json.dumps(modify_res, indent=4))

        proc_section_step_2_1_a = modify_res['elem']
        numbers = modify_res['numbers']
        elem_ids = modify_res['elem_ids']
        proc_section_step_2_1_a_id = proc_section_step_2_1_a['elem_id']               

        self.assertEqual(proc_section_step_2_1_a['number'], '2-1.a')
        self.assertEqual(proc_section_step_2_1_a['procedure_modification_status'], 'MODIFYING')
        self.assertEqual(proc_section_step_2_1_a['procedure_modification']['justification']['modification_type'], 'REDLINE')

        self.assertEqual(len(numbers), 2)
        self.assertEqual(numbers[0]['elem_id'], proc_section_step_2_1_id)
        self.assertEqual(numbers[0]['number'], '2-1')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'MODIFIED')
        self.assertEqual(numbers[1]['elem_id'], proc_section_step_2_1_a_id)
        self.assertEqual(numbers[1]['number'], '2-1.a')
        self.assertEqual(numbers[1]['procedure_modification_status'], 'MODIFYING')     
        self.assertEqual(len(elem_ids), 9)   

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))    
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')            
        self.assertEqual(elements_res[6]['number'], '2-1') 
        self.assertEqual(elements_res[6]['procedure_modification_status'], 'MODIFIED')       
        self.assertEqual(elements_res[7]['number'], '2-1.a')  
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'MODIFYING')
        self.assertEqual(elements_res[8]['number'], '2-2')

        # set justification
        justification_input = {
            'procedure_modification': {
                'justification': {
                    'modification_type': 'BLUELINE',                    
                    'content': 'this is a temporary change',
                    'user_name': 'hongmank',
                    'time_updated': '2018-08-09T15:42:01.416Z'
                }
            }
        }
        res = self.update_element(execution_url, proc_section_step_2_1_a_id, justification_input)
        self.assertDictEqual(res['procedure_modification']['justification'], justification_input['procedure_modification']['justification'])
        
        # approve it
        approval_input = {
            'procedure_modification': {
                'approval': {                 
                    'content': 'this is a temporary change',
                    'user_name': 'hongmank',
                    'time_updated': '2018-08-09T16:42:01.416Z',
                    'status': 'APPROVED'
                }
            }
        }
        res = self.update_element(execution_url, proc_section_step_2_1_a_id, approval_input)
        self.assertDictEqual(res['procedure_modification']['approval'], approval_input['procedure_modification']['approval'])        

        # modify the step again

        modify_res = self.modify_element(execution_id, proc_section_step_2_1_id)
        logger.debug('modify_res= %s', json.dumps(modify_res, indent=4))

        proc_section_step_2_1_b = modify_res['elem']
        numbers = modify_res['numbers']
        elem_ids = modify_res['elem_ids']
        proc_section_step_2_1_b_id = proc_section_step_2_1_b['elem_id']               

        self.assertEqual(proc_section_step_2_1_b['number'], '2-1.b')
        self.assertEqual(proc_section_step_2_1_b['procedure_modification_status'], 'MODIFYING')
        self.assertEqual(proc_section_step_2_1_b['procedure_modification']['justification']['modification_type'], 'REDLINE')

        self.assertEqual(len(numbers), 2)
        self.assertEqual(numbers[0]['elem_id'], proc_section_step_2_1_a_id)
        self.assertEqual(numbers[0]['number'], '2-1.a')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'MODIFYING_OLD')   
        self.assertEqual(numbers[1]['elem_id'], proc_section_step_2_1_b_id)
        self.assertEqual(numbers[1]['number'], '2-1.b')
        self.assertEqual(numbers[1]['procedure_modification_status'], 'MODIFYING')         

        self.assertEqual(len(elem_ids), 10)   

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))    
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')            
        self.assertEqual(elements_res[6]['number'], '2-1') 
        self.assertEqual(elements_res[6]['procedure_modification_status'], 'MODIFIED')       
        self.assertEqual(elements_res[7]['number'], '2-1.a')  
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'MODIFYING_OLD')
        self.assertEqual(elements_res[8]['number'], '2-1.b')  
        self.assertEqual(elements_res[8]['procedure_modification_status'], 'MODIFYING')        
        self.assertEqual(elements_res[9]['number'], '2-2')        
        self.assertEqual(elements_res[9]['procedure_modification_status'], 'ORIGINAL')
        
        # modify the step 3rd time

        modify_res = self.modify_element(execution_id, proc_section_step_2_1_id)
        logger.debug('modify_res= %s', json.dumps(modify_res, indent=4))

        proc_section_step_2_1_c = modify_res['elem']
        numbers = modify_res['numbers']
        elem_ids = modify_res['elem_ids']
        proc_section_step_2_1_c_id = proc_section_step_2_1_c['elem_id']               

        self.assertEqual(proc_section_step_2_1_c['number'], '2-1.c')
        self.assertEqual(proc_section_step_2_1_c['procedure_modification_status'], 'MODIFYING')
        self.assertEqual(proc_section_step_2_1_c['procedure_modification']['justification']['modification_type'], 'REDLINE')

        self.assertEqual(len(numbers), 2)   
        self.assertEqual(numbers[0]['elem_id'], proc_section_step_2_1_b_id)
        self.assertEqual(numbers[0]['number'], '2-1.b')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'MODIFYING_OLD')   
        self.assertEqual(numbers[1]['elem_id'], proc_section_step_2_1_c_id)
        self.assertEqual(numbers[1]['number'], '2-1.c')
        self.assertEqual(numbers[1]['procedure_modification_status'], 'MODIFYING')              

        self.assertEqual(len(elem_ids), 11)   

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))    
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')            
        self.assertEqual(elements_res[6]['number'], '2-1') 
        self.assertEqual(elements_res[6]['procedure_modification_status'], 'MODIFIED')       
        self.assertEqual(elements_res[7]['number'], '2-1.a')  
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'MODIFYING_OLD')
        self.assertEqual(elements_res[8]['number'], '2-1.b')  
        self.assertEqual(elements_res[8]['procedure_modification_status'], 'MODIFYING_OLD')  
        self.assertEqual(elements_res[9]['number'], '2-1.c')  
        self.assertEqual(elements_res[9]['procedure_modification_status'], 'MODIFYING')              
        self.assertEqual(elements_res[10]['number'], '2-2')        
        self.assertEqual(elements_res[10]['procedure_modification_status'], 'ORIGINAL')            

        # discard redline C
        dicard_res = self.discard_element(execution_id, proc_section_step_2_1_c_id, 200)  
        logger.debug('dicard_res= %s', json.dumps(dicard_res, indent=4))       
        numbers = dicard_res['numbers']
        elem_ids = dicard_res['elem_ids']         
        
        self.assertEqual(len(numbers), 1)   
        self.assertEqual(numbers[0]['elem_id'], proc_section_step_2_1_b_id)
        self.assertEqual(numbers[0]['number'], '2-1.b')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'MODIFYING')               

        self.assertEqual(len(elem_ids), 10)   

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))    
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')            
        self.assertEqual(elements_res[6]['number'], '2-1') 
        self.assertEqual(elements_res[6]['procedure_modification_status'], 'MODIFIED')       
        self.assertEqual(elements_res[7]['number'], '2-1.a')  
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'MODIFYING_OLD')
        self.assertEqual(elements_res[8]['number'], '2-1.b')  
        self.assertEqual(elements_res[8]['procedure_modification_status'], 'MODIFYING')        
        self.assertEqual(elements_res[9]['number'], '2-2')        
        self.assertEqual(elements_res[9]['procedure_modification_status'], 'ORIGINAL')

        res = self.add_paragraph(base_url=execution_url,
            insert_after_id=proc_section_step_1_2_id,
            level='SIBLING',
            title='Paragraph 1-2.1 in Procedure Section')
        logger.debug('res= %s', json.dumps(res, indent=4))
        proc_section_paragraph_1_2__1 = res['elem']
        numbers = res['numbers']
        elem_ids = res['elem_ids']
        proc_section_paragraph_1_2__1_id = proc_section_paragraph_1_2__1['elem_id']        
        self.assertEqual(proc_section_paragraph_1_2__1['procedure_section_id'], procedure_section_id)         
        self.assertEqual(proc_section_paragraph_1_2__1['procedure_title'], procedure_title)  
        self.assertEqual(proc_section_paragraph_1_2__1['procedure_id'], procedure_id)  

        self.assertEqual(proc_section_paragraph_1_2__1['procedure_section_id'], procedure_section_id)         
        self.assertEqual(proc_section_paragraph_1_2__1['procedure_title'], procedure_title)  
        self.assertEqual(proc_section_paragraph_1_2__1['procedure_id'], procedure_id)          

        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0]['elem_id'], proc_section_paragraph_1_2__1_id)
        self.assertEqual(numbers[0]['number'], '1-2.1')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'ADDED') 
        self.assertEqual(len(elem_ids), 11)           

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))     
        self.assertEqual(elements_res[3]['number'], '1-2') 
        self.assertEqual(elements_res[3]['procedure_modification_status'], 'ORIGINAL')   
        self.assertEqual(elements_res[4]['number'], '1-2.1') 
        self.assertEqual(elements_res[4]['procedure_modification_status'], 'ADDED')               
        self.assertEqual(elements_res[7]['number'], '2-1') 
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'MODIFIED')       
        self.assertEqual(elements_res[8]['number'], '2-1.a')  
        self.assertEqual(elements_res[8]['procedure_modification_status'], 'MODIFYING_OLD')
        self.assertEqual(elements_res[9]['number'], '2-1.b')  
        self.assertEqual(elements_res[9]['procedure_modification_status'], 'MODIFYING')          
        self.assertEqual(elements_res[10]['number'], '2-2')
        self.assertEqual(elements_res[10]['procedure_modification_status'], 'ORIGINAL')
 
        # delete a step to create a redline
        res = self.delete_element(execution_url, proc_section_step_1_2_id)
        logger.debug('res= %s', json.dumps(res, indent=4))
        numbers = res['numbers']
        elem_ids = res['elem_ids']    
        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0]['elem_id'], proc_section_step_1_2_id)
        self.assertEqual(numbers[0]['number'], '1-2')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'DELETED')     
        self.assertEqual(len(elem_ids), 11)   

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))              
        self.assertEqual(elements_res[3]['number'], '1-2') 
        self.assertEqual(elements_res[3]['procedure_modification_status'], 'DELETED')   
        self.assertEqual(elements_res[4]['number'], '1-2.1') 
        self.assertEqual(elements_res[4]['procedure_modification_status'], 'ADDED')               
        self.assertEqual(elements_res[7]['number'], '2-1') 
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'MODIFIED')       
        self.assertEqual(elements_res[8]['number'], '2-1.a')  
        self.assertEqual(elements_res[8]['procedure_modification_status'], 'MODIFYING_OLD')
        self.assertEqual(elements_res[9]['number'], '2-1.b')  
        self.assertEqual(elements_res[9]['procedure_modification_status'], 'MODIFYING') 
        self.assertEqual(elements_res[10]['number'], '2-2')   
        self.assertEqual(elements_res[10]['procedure_modification_status'], 'ORIGINAL')        

        # set justification
        justification_input = {
            'procedure_modification': {
                'justification': {
                    'modification_type': 'REDLINE',                    
                    'content': 'this step is not needed',
                    'user_name': 'hongmank',
                    'time_updated': '2018-08-09T15:42:01.416Z'
                }
            }
        }
        res = self.update_element(execution_url, proc_section_step_1_2_id, justification_input)
        logger.debug('res= %s', json.dumps(res, indent=4))
        self.assertDictEqual(res['procedure_modification']['justification'], justification_input['procedure_modification']['justification'])          

        # copy a step to create a redline
        res = self.copy_element(base_url=execution_url,
            elem_id=proc_section_step_1_3_id, insert_after_id=proc_section_step_2_1_b_id, level='SIBLING',
            code_expected=200)
        logger.debug('copy_element res: %s', json.dumps(res, indent=4))  
        self.assertEqual(len(res['elements']), 1) 
        proc_section_step_2_1__1 = res['elements'][0] 
        proc_section_step_2_1__1_id = proc_section_step_2_1__1['elem_id']
        numbers = res['numbers']
        elem_ids = res['elem_ids']    
        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0]['elem_id'], proc_section_step_2_1__1_id)
        self.assertEqual(numbers[0]['number'], '2-1.1')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'ADDED')     
        self.assertEqual(len(elem_ids), 12) 

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))  
        self.assertEqual(elements_res[3]['number'], '1-2') 
        self.assertEqual(elements_res[3]['procedure_modification_status'], 'DELETED')   
        self.assertEqual(elements_res[4]['number'], '1-2.1') 
        self.assertEqual(elements_res[4]['procedure_modification_status'], 'ADDED')               
        self.assertEqual(elements_res[7]['number'], '2-1') 
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'MODIFIED')       
        self.assertEqual(elements_res[8]['number'], '2-1.a')  
        self.assertEqual(elements_res[8]['procedure_modification_status'], 'MODIFYING_OLD')
        self.assertEqual(elements_res[9]['number'], '2-1.b')  
        self.assertEqual(elements_res[9]['procedure_modification_status'], 'MODIFYING') 
        self.assertEqual(elements_res[10]['number'], '2-1.1')  
        self.assertEqual(elements_res[10]['procedure_modification_status'], 'ADDED')
        self.assertEqual(elements_res[10]['title'], 'Step 1-3')        
        self.assertEqual(elements_res[11]['number'], '2-2')        
        self.assertEqual(elements_res[11]['procedure_modification_status'], 'ORIGINAL')    

        # add a paragraph as the first element to create a redline
        res = self.add_paragraph(base_url=execution_url,
            insert_after_id=procedure_section_id,
            level='CHILD',
            title='Paragraph 0.1 in Procedure Section')

        logger.debug('res= %s', json.dumps(res, indent=4))
        proc_section_paragraph_0__1 = res['elem']
        numbers = res['numbers']
        elem_ids = res['elem_ids']
        proc_section_paragraph_0__1_id = proc_section_paragraph_0__1['elem_id']        

        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0]['elem_id'], proc_section_paragraph_0__1_id)
        self.assertEqual(numbers[0]['number'], '0.1')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'ADDED')     
        self.assertEqual(len(elem_ids), 13)           

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))    
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')   
        self.assertEqual(elements_res[1]['number'], '0.1') 
        self.assertEqual(elements_res[1]['procedure_modification_status'], 'ADDED') 
        self.assertEqual(elements_res[2]['number'], '1') 
        self.assertEqual(elements_res[2]['procedure_modification_status'], 'ORIGINAL')                   


        res = self.add_paragraph(base_url=execution_url,
            insert_after_id=proc_section_paragraph_0__1_id,
            level='SIBLING',
            title='Paragraph 0.2 in Procedure Section')

        logger.debug('res= %s', json.dumps(res, indent=4))
        proc_section_paragraph_0__2 = res['elem']
        numbers = res['numbers']
        elem_ids = res['elem_ids']
        proc_section_paragraph_0__2_id = proc_section_paragraph_0__2['elem_id']        

        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0]['elem_id'], proc_section_paragraph_0__2_id)
        self.assertEqual(numbers[0]['number'], '0.2')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'ADDED')     
        self.assertEqual(len(elem_ids), 14)           

        elements_res = self.get_elements(execution_url)

        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))      
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')   
        self.assertEqual(elements_res[1]['number'], '0.1') 
        self.assertEqual(elements_res[1]['procedure_modification_status'], 'ADDED') 
        self.assertEqual(elements_res[2]['number'], '0.2') 
        self.assertEqual(elements_res[2]['procedure_modification_status'], 'ADDED')         
        self.assertEqual(elements_res[3]['number'], '1') 
        self.assertEqual(elements_res[3]['procedure_modification_status'], 'ORIGINAL')   

        # discard the ones added at the front
        res = self.discard_element(execution_id, proc_section_paragraph_0__1_id, 200)  
        logger.debug('res= %s', json.dumps(res, indent=4))        

        res = self.discard_element(execution_id, proc_section_paragraph_0__2_id, 200)  

        logger.debug('res= %s', json.dumps(res, indent=4))                              

        if not complete:
            return

        ## test various rules that would prevent element operations 
        
        # Add a section temporarily   
        res = self.add_section(base_url=execution_url,
            insert_after_id=procedure_section_id,
            level='SIBLING',
            title='Temporary section')
        logger.debug('add_section res= %s', json.dumps(res, indent=4))
        section_2_id = res['elem']['elem_id']

        # Add a paragraph temporarily   
        res = self.add_paragraph(base_url=execution_url,
            insert_after_id=section_2_id,
            level='SIBLING',
            title='Temporary paragraph')
        logger.debug('add_paragraph res= %s', json.dumps(res, indent=4))
        paragraph_3_id = res['elem']['elem_id']        

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4)) 
        
        # copy a redline element into a non-protected area
        res = self.copy_element(base_url=execution_url,
            elem_id=proc_section_step_2_1_a_id, insert_after_id=paragraph_3_id, level='SIBLING',
            code_expected=200)
        logger.debug('copy_element res: %s', json.dumps(res, indent=4))  

        self.assertEqual(len(res['elements']), 1) 
        step_4 = res['elements'][0] 
        step_4_id = step_4['elem_id']
        numbers = res['numbers']
        elem_ids = res['elem_ids']   
        self.assertEqual(step_4['number'], '4')
        self.assertEqual(step_4['procedure_modification_status'], 'NONE')
        self.assertDictEqual(step_4['procedure_modification'], {})

        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0]['elem_id'], step_4_id)
        self.assertEqual(numbers[0]['number'], '4')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'NONE')     
        
        self.assertEqual(len(elem_ids), 15) 

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))   
        self.assertEqual(elements_res[14]['elem_id'], step_4_id) 
        self.assertEqual(elements_res[14]['number'], '4')        
        self.assertEqual(elements_res[14]['procedure_modification_status'], 'NONE')        
        self.assertEqual(elements_res[14]['procedure_section_id'], '') 
        self.assertEqual(elements_res[14]['procedure_id'], '') 
        self.assertEqual(elements_res[14]['procedure_title'], '')                              
            
        # Cannot add section    
        res = self.add_section(base_url=execution_url,
            insert_after_id=proc_section_step_2_1_id,
            level='SIBLING',
            title='Section cannot be added',
            code_expected=400)
        logger.debug('res= %s', json.dumps(res, indent=4))

        # Cannot add between modified elements    
        res = self.add_paragraph(base_url=execution_url,
            insert_after_id=proc_section_step_2_1_id,
            level='SIBLING',
            title='Paragraph cannot be added',
            code_expected=400)
        logger.debug('res= %s', json.dumps(res, indent=4))

        # Cannot add between modified elements    
        res = self.add_paragraph(base_url=execution_url,
            insert_after_id=proc_section_step_2_1_a_id,
            level='SIBLING',
            title='Paragraph cannot be added',
            code_expected=400)
        logger.debug('res= %s', json.dumps(res, indent=4))      

        # Cannot move into protected area          
        logger.debug('proc_section_paragraph_1_1_id= %s', proc_section_paragraph_1_1_id) 
        res = self.move_element(base_url=execution_url,
            elem_id=section_2_id,
            insert_after_id=proc_section_paragraph_1_1_id,
            level='SIBLING',
            code_expected=400)
        logger.debug('move res= %s', json.dumps(res, indent=4))

        # Cannot move out from protected area
        res = self.move_element(base_url=execution_url,
            elem_id=proc_section_step_2_1_a_id,
            insert_after_id=section_2_id,
            level='SIBLING',
            code_expected=400)       
        logger.debug('move res= %s', json.dumps(res, indent=4)) 

        # Can copy a section into the protected area
        res = self.copy_element(base_url=execution_url,
            elem_id=section_2_id,
            insert_after_id=proc_section_paragraph_1_1_id,
            level='SIBLING',
            code_expected=200)       
        logger.debug('copy res= %s', json.dumps(res, indent=4))     

        # cannot discard a section
        self.discard_element(execution_id, res['numbers'][0]['elem_id'], 400)   

        # can delete a section
        res = self.delete_element(execution_url, res['numbers'][0]['elem_id'])  
        logger.debug('res= %s', json.dumps(res, indent=4)) 

        # Cannot copy a procedure section that has been imported into the protected area
        res = self.copy_element(base_url=execution_url,
            elem_id=procedure_section_id,
            insert_after_id=proc_section_paragraph_1_1_id,
            level='SIBLING',
            code_expected=400)       
        logger.debug('copy res= %s', json.dumps(res, indent=4))              

        # Cannot copy to between modified elements    
        res = self.copy_element(base_url=execution_url,
            elem_id=paragraph_3_id,
            insert_after_id=proc_section_step_2_1_id,
            level='SIBLING',
            code_expected=400)
        logger.debug('res= %s', json.dumps(res, indent=4))

        # Cannot copy to between modified elements    
        res = self.copy_element(base_url=execution_url,
            elem_id=paragraph_3_id,        
            insert_after_id=proc_section_step_2_1_a_id,
            level='SIBLING',
            code_expected=400)
        logger.debug('res= %s', json.dumps(res, indent=4))   


        # We are done with the section, remove it. 
        self.delete_element(execution_url, section_2_id) 
        self.delete_element(execution_url, paragraph_3_id) 
        self.delete_element(execution_url, step_4_id)
        
        # Cannot delete a redline element
        res = self.delete_element(execution_url, proc_section_step_2_1_a_id, 400)  
        logger.debug('res= %s', json.dumps(res, indent=4)) 

        # return

        # Cannot discard NONE
        res = self.discard_element(execution_id, procedure_section_id, 400)  
        logger.debug('res= %s', json.dumps(res, indent=4)) 

        # Cannot discard ORIGINAL
        res = self.discard_element(execution_id, proc_section_section_1_id, 400)  
        logger.debug('res= %s', json.dumps(res, indent=4)) 

        # Cannot discard MODIFYING_OLD
        res = self.discard_element(execution_id, proc_section_step_2_1_a_id, 400)  
        logger.debug('res= %s', json.dumps(res, indent=4)) 

        # Cannot discard MODIFIED
        res = self.discard_element(execution_id, proc_section_step_2_1_id, 400)   
        logger.debug('res= %s', json.dumps(res, indent=4))

        # Can discard MODIFYING
        res = self.discard_element(execution_id, proc_section_step_2_1_b_id)       
        logger.debug('res= %s', json.dumps(res, indent=4))
        numbers = res['numbers']
        elem_ids = res['elem_ids']    
        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0]['elem_id'], proc_section_step_2_1_a_id)
        self.assertEqual(numbers[0]['number'], '2-1.a')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'MODIFYING')     
        self.assertEqual(len(elem_ids), 11)         

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))  
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')    
        self.assertEqual(elements_res[1]['number'], '1') 
        self.assertEqual(elements_res[1]['procedure_modification_status'], 'ORIGINAL') 
        self.assertEqual(elements_res[2]['number'], '1-1') 
        self.assertEqual(elements_res[2]['procedure_modification_status'], 'ORIGINAL')                     
        self.assertEqual(elements_res[3]['number'], '1-2') 
        self.assertEqual(elements_res[3]['procedure_modification_status'], 'DELETED')   
        self.assertEqual(elements_res[4]['number'], '1-2.1') 
        self.assertEqual(elements_res[4]['procedure_modification_status'], 'ADDED')  
        self.assertEqual(elements_res[5]['number'], '1-3') 
        self.assertEqual(elements_res[5]['procedure_modification_status'], 'ORIGINAL')          
        self.assertEqual(elements_res[6]['number'], '2') 
        self.assertEqual(elements_res[6]['procedure_modification_status'], 'ORIGINAL')                    
        self.assertEqual(elements_res[7]['number'], '2-1') 
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'MODIFIED')       
        self.assertEqual(elements_res[8]['number'], '2-1.a')  
        self.assertEqual(elements_res[8]['procedure_modification_status'], 'MODIFYING')
        self.assertEqual(elements_res[9]['number'], '2-1.1')  
        self.assertEqual(elements_res[9]['procedure_modification_status'], 'ADDED')       
        self.assertEqual(elements_res[10]['number'], '2-2')        
        self.assertEqual(elements_res[10]['procedure_modification_status'], 'ORIGINAL')    

        # Cannot discard an approved element
        res = self.discard_element(execution_id, proc_section_step_2_1_a_id, 400)       
        logger.debug('res= %s', json.dumps(res, indent=4))

        # unapprove it
        approval_input = {
            'procedure_modification': {
                'approval': {                 
                    'content': 'this is a temporary change',
                    'user_name': 'hongmank',
                    'time_updated': '2018-08-09T16:42:01.416Z',
                    'status': 'PENDING'
                }
            }
        }
        res = self.update_element(execution_url, proc_section_step_2_1_a_id, approval_input)
        self.assertDictEqual(res['procedure_modification']['approval'], approval_input['procedure_modification']['approval'])           

        # Can discard MODIFYING again
        res = self.discard_element(execution_id, proc_section_step_2_1_a_id)       
        logger.debug('res= %s', json.dumps(res, indent=4))
        numbers = res['numbers']
        elem_ids = res['elem_ids']    
        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0]['elem_id'], proc_section_step_2_1_id)
        self.assertEqual(numbers[0]['number'], '2-1')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'ORIGINAL')     
        self.assertEqual(len(elem_ids), 10)         

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))  
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')    
        self.assertEqual(elements_res[1]['number'], '1') 
        self.assertEqual(elements_res[1]['procedure_modification_status'], 'ORIGINAL') 
        self.assertEqual(elements_res[2]['number'], '1-1') 
        self.assertEqual(elements_res[2]['procedure_modification_status'], 'ORIGINAL')                     
        self.assertEqual(elements_res[3]['number'], '1-2') 
        self.assertEqual(elements_res[3]['procedure_modification_status'], 'DELETED')   
        self.assertEqual(elements_res[4]['number'], '1-2.1') 
        self.assertEqual(elements_res[4]['procedure_modification_status'], 'ADDED')  
        self.assertEqual(elements_res[5]['number'], '1-3') 
        self.assertEqual(elements_res[5]['procedure_modification_status'], 'ORIGINAL')          
        self.assertEqual(elements_res[6]['number'], '2') 
        self.assertEqual(elements_res[6]['procedure_modification_status'], 'ORIGINAL')                    
        self.assertEqual(elements_res[7]['number'], '2-1') 
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'ORIGINAL')       
        self.assertEqual(elements_res[8]['number'], '2-1.1')  
        self.assertEqual(elements_res[8]['procedure_modification_status'], 'ADDED')       
        self.assertEqual(elements_res[9]['number'], '2-2')        
        self.assertEqual(elements_res[9]['procedure_modification_status'], 'ORIGINAL')         

        # Can discard ADDED
        res = self.discard_element(execution_id, proc_section_paragraph_1_2__1_id)       
        logger.debug('res= %s', json.dumps(res, indent=4))
        numbers = res['numbers']
        elem_ids = res['elem_ids']    
        self.assertEqual(len(numbers), 0)  
        self.assertEqual(len(elem_ids), 9)         

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))  
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')    
        self.assertEqual(elements_res[1]['number'], '1') 
        self.assertEqual(elements_res[1]['procedure_modification_status'], 'ORIGINAL') 
        self.assertEqual(elements_res[2]['number'], '1-1') 
        self.assertEqual(elements_res[2]['procedure_modification_status'], 'ORIGINAL')                     
        self.assertEqual(elements_res[3]['number'], '1-2') 
        self.assertEqual(elements_res[3]['procedure_modification_status'], 'DELETED')   
        self.assertEqual(elements_res[4]['number'], '1-3') 
        self.assertEqual(elements_res[4]['procedure_modification_status'], 'ORIGINAL')          
        self.assertEqual(elements_res[5]['number'], '2') 
        self.assertEqual(elements_res[5]['procedure_modification_status'], 'ORIGINAL')                    
        self.assertEqual(elements_res[6]['number'], '2-1') 
        self.assertEqual(elements_res[6]['procedure_modification_status'], 'ORIGINAL')       
        self.assertEqual(elements_res[7]['number'], '2-1.1')  
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'ADDED')       
        self.assertEqual(elements_res[8]['number'], '2-2')        
        self.assertEqual(elements_res[8]['procedure_modification_status'], 'ORIGINAL')    

        # Can discard another ADDED
        res = self.discard_element(execution_id, proc_section_step_2_1__1_id)       
        logger.debug('res= %s', json.dumps(res, indent=4))
        numbers = res['numbers']
        elem_ids = res['elem_ids']    
        self.assertEqual(len(numbers), 0)  
        self.assertEqual(len(elem_ids), 8)         

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))  
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')    
        self.assertEqual(elements_res[1]['number'], '1') 
        self.assertEqual(elements_res[1]['procedure_modification_status'], 'ORIGINAL') 
        self.assertEqual(elements_res[2]['number'], '1-1') 
        self.assertEqual(elements_res[2]['procedure_modification_status'], 'ORIGINAL')                     
        self.assertEqual(elements_res[3]['number'], '1-2') 
        self.assertEqual(elements_res[3]['procedure_modification_status'], 'DELETED')   
        self.assertEqual(elements_res[4]['number'], '1-3') 
        self.assertEqual(elements_res[4]['procedure_modification_status'], 'ORIGINAL')          
        self.assertEqual(elements_res[5]['number'], '2') 
        self.assertEqual(elements_res[5]['procedure_modification_status'], 'ORIGINAL')                    
        self.assertEqual(elements_res[6]['number'], '2-1') 
        self.assertEqual(elements_res[6]['procedure_modification_status'], 'ORIGINAL')              
        self.assertEqual(elements_res[7]['number'], '2-2')        
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'ORIGINAL')       

        # Can discard DELETED
        res = self.discard_element(execution_id, proc_section_step_1_2_id)       
        logger.debug('res= %s', json.dumps(res, indent=4))
        numbers = res['numbers']
        elem_ids = res['elem_ids']    
        self.assertEqual(len(numbers), 1)
        self.assertEqual(numbers[0]['elem_id'], proc_section_step_1_2_id)
        self.assertEqual(numbers[0]['number'], '1-2')
        self.assertEqual(numbers[0]['procedure_modification_status'], 'ORIGINAL')   
        self.assertEqual(len(elem_ids), 8)         

        elements_res = self.get_elements(execution_url)
        logger.debug('elements_res= %s', json.dumps(elements_res, indent=4))  
        self.assertEqual(elements_res[0]['number'], '1') 
        self.assertEqual(elements_res[0]['procedure_modification_status'], 'NONE')    
        self.assertEqual(elements_res[1]['number'], '1') 
        self.assertEqual(elements_res[1]['procedure_modification_status'], 'ORIGINAL') 
        self.assertEqual(elements_res[2]['number'], '1-1') 
        self.assertEqual(elements_res[2]['procedure_modification_status'], 'ORIGINAL')                     
        self.assertEqual(elements_res[3]['number'], '1-2') 
        self.assertEqual(elements_res[3]['procedure_modification_status'], 'ORIGINAL') 
        self.assertDictEqual(elements_res[3]['procedure_modification'], {})
        self.assertEqual(elements_res[4]['number'], '1-3') 
        self.assertEqual(elements_res[4]['procedure_modification_status'], 'ORIGINAL')          
        self.assertEqual(elements_res[5]['number'], '2') 
        self.assertEqual(elements_res[5]['procedure_modification_status'], 'ORIGINAL')                    
        self.assertEqual(elements_res[6]['number'], '2-1') 
        self.assertEqual(elements_res[6]['procedure_modification_status'], 'ORIGINAL')              
        self.assertEqual(elements_res[7]['number'], '2-2')        
        self.assertEqual(elements_res[7]['procedure_modification_status'], 'ORIGINAL')   


    def check_as_run(self, res_dict):
        self.assertEqual(res_dict['children'][0]['title'], 'Section 1')
        self.assertEqual(res_dict['children'][0]['number'], '1')
        self.assertEqual(res_dict['children'][0]['children'][0]['title'], 'Step 1-1')
        self.assertEqual(res_dict['children'][0]['children'][0]['number'], '1-1')
        self.assertEqual(res_dict['children'][0]['children'][1]['title'], 'Step 1-2')
        self.assertEqual(res_dict['children'][0]['children'][1]['number'], '1-2')
        self.assertEqual(res_dict['children'][1]['title'], 'Paragraph Section 1')
        self.assertEqual(res_dict['children'][1]['number'], '2')     # paragraph should not be numbered
        self.assertEqual(res_dict['children'][2]['title'], 'Section 3')
        self.assertEqual(res_dict['children'][2]['number'], '3')
        self.assertEqual(res_dict['children'][2]['children'][0]['title'], 'Step 3-1')
        self.assertEqual(res_dict['children'][2]['children'][0]['number'], '3-1')
        self.assertEqual(res_dict['children'][2]['children'][1]['title'], 'Step 3-2')
        self.assertEqual(res_dict['children'][2]['children'][1]['number'], '3-2')


    def test_get_executions(self):
        ## Add executions with unique description
        random_name1 = random_string(8)
        random_name2 = random_string(8)

        procedure_title_1 = 'My procedure 1 ' + random_name1
        procedure_description_1 = 'My procedure 1 description ' + random_name1
        institutional_id_1 = 'ins_1_' + random_name1
        institutional_release_id_1_1 = 'rel_1_1_' + random_name1

        procedure_title_2 = 'My procedure 2 ' + random_name2
        procedure_description_2 = 'My procedure 2 description ' + random_name2
        institutional_id_2 = 'ins_2_' + random_name2
        institutional_release_id_2_1 = 'rel_2_1_' + random_name2

        procedure_1 = self.create_procedure(procedure_title_1, procedure_description_1,
            institutional_id_1, 'hkim')
        procedure_id_1 = procedure_1['procedure_id']

        self.create_procedure_version(procedure_id_1, 'version 1', 'hkim')
        self.update_procedure_version(procedure_id_1, 1, {'institutional_release_id': institutional_release_id_1_1})
        self.update_procedure_version_status(procedure_id_1, 1, {'action': 'RELEASE'})
        self.create_procedure_version(procedure_id_1, 'version 2', 'hkim')

        procedure_2 = self.create_procedure(procedure_title_2, procedure_description_2,
            institutional_id_2, 'hkim')
        procedure_id_2 = procedure_2['procedure_id']

        procedure_2_version_1 = self.create_procedure_version(procedure_id_2, 'version 1', 'hkim')
        self.update_procedure_version(procedure_id_2, 1, {'institutional_release_id': institutional_release_id_2_1})
        self.update_procedure_version_status(procedure_id_2, 1, {'action': 'RELEASE'})

        description1 = 'My execution 1 name ' + random_name1
        venue_id_1, venue_name_1 = self.create_venue2('WSTS')
        execution_dict = self.create_execution(venue_id_1, description1)
        execution_id_1 = execution_dict['execution_id']
        time_started_1 = execution_dict['time_started']
        test_conductor_1 = 'hpotter_' + random_name1
        test_conductor_2 = 'hsimpson_' + random_name2
        self.update_execution(execution_id_1,
            {
                'test_conductors': [test_conductor_1],
                'time_completed': '',
                'used_procedures': []
            },
            code_expected=200
        )
        time.sleep(0.01)   # To make it sure create time is different

        description2 = 'My execution 2 name ' + random_name1
        venue_id_2, venue_name_2 = self.create_venue2('WSTS')
        execution_dict = self.create_execution(venue_id_2, description2)
        execution_id_2 = execution_dict['execution_id']
        time_started_2 = execution_dict['time_started']
        self.update_execution(execution_id_2,
            {
                'test_conductors': [test_conductor_1, test_conductor_2],
                'time_completed': '2018-04-25T21:39:24.232Z',
                'used_procedures': []
            },
            code_expected=200
        )
        time.sleep(0.01)   # To make it sure create time is different

        description3 = 'My execution 3 name ' + random_name2
        venue_id_3, venue_name_3 = self.create_venue2('Testbed')
        execution_dict = self.create_execution(venue_id_3, description3)
        execution_id_3 = execution_dict['execution_id']
        time_started_3 = execution_dict['time_started']
        self.update_execution(execution_id_3,
            {
                'test_conductors': [test_conductor_2],
                'time_completed': '2018-04-26T21:39:24.232Z',
                'status': 'IDLE',
                'used_procedures': [
                    {
                        'procedure_id': procedure_id_1, 
                        'version': 1, 
                        'institutional_id': institutional_id_1,
                        'institutional_release_id': institutional_release_id_1_1
                    }
                ]
            },
            code_expected=200
        )
        time.sleep(0.01)   # To make it sure create time is different

        description4 = 'My execution 4 name ' + random_name2
        venue_id_4, venue_name_4 = self.create_venue2('Testbed')
        execution_dict = self.create_execution(venue_id_4, description4)
        execution_id_4 = execution_dict['execution_id']
        self.update_execution(execution_id_4,
            {
                'test_conductors': [test_conductor_2],
                'time_completed': '2018-04-27T21:39:24.232Z',
                'status': 'RUNNING',
                'used_procedures': [
                    {
                        'procedure_id': procedure_id_1, 
                        'version': 2,
                        'institutional_id': institutional_id_1,
                        'institutional_release_id': ''
                    },
                    {
                        'procedure_id': procedure_id_2, 
                        'version': 1,
                        'institutional_id': institutional_id_2,
                        'institutional_release_id': institutional_release_id_2_1
                    }
                ]
            },
            code_expected=200
        )
        time.sleep(0.01)   # To make it sure create time is different

        description5 = 'My execution 5 name ' + random_name2
        venue_id_5, venue_name_5 = self.create_venue2('ATLO')
        execution_dict = self.create_execution(venue_id_5, description5)
        execution_id_5 = execution_dict['execution_id']
        self.update_execution(execution_id_5,
            {
                'test_conductors': [test_conductor_2],
                'time_completed': '2018-04-28T21:39:24.232Z',
                'status': 'CLOSED',
                'used_procedures': [
                    {
                        'procedure_id': procedure_id_1, 
                        'version': 1,
                        'institutional_id': institutional_id_1,
                        'institutional_release_id': institutional_release_id_1_1                        
                    },
                    {
                        'procedure_id': procedure_id_2, 
                        'version': 1,
                        'institutional_id': institutional_id_2,
                        'institutional_release_id': institutional_release_id_2_1                        
                    }
                ]
            },
            code_expected=200
        )
        time.sleep(0.01)   # To make it sure create time is different

        ## Get executions
        url = shared_dict['host'] + '/executions'
        result = requests.get(url, headers=shared_dict['headers'])
        # print('result.status_code=', result.status_code)
        # print('result.text=', result.text)
        self.assertEqual(result.status_code, 200)
        executions_dict = json.loads(result.text)
        # print 'executions_dict=', json.dumps(executions_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertGreater(len(executions_dict), 0)

        ## Get executions in ASC order
        url = shared_dict['host'] + '/executions'
        params = {'sort': 'ASC'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        executions_dict_asc = json.loads(result.text)
        # print 'executions_dict_asc=', json.dumps(executions_dict_asc, indent=4)
        self.assertGreater(len(executions_dict), 0)

        ## Get executions in DESC order
        url = shared_dict['host'] + '/executions'
        params = {'sort': 'DESC'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        executions_dict_desc = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertGreater(len(executions_dict), 0)

        # The default sorting is DESC
        self.assertEqual(executions_dict[0]['execution_id'], executions_dict_desc[0]['execution_id'])
        self.assertEqual(executions_dict[-1]['execution_id'], executions_dict_desc[-1]['execution_id'])

        if len(executions_dict_desc) < 50:
            # This makes sense only the total count is less than 50 which is the default return size
            # Check the sorting
            self.assertEqual(executions_dict_asc[0]['execution_id'], executions_dict_desc[-1]['execution_id'])
            self.assertEqual(executions_dict_asc[-1]['execution_id'], executions_dict_desc[0]['execution_id'])

        ## sort by EXECUTION_ID ASC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'ASC', 'sort_by': 'EXECUTION_ID'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        self.assertEqual(res_dict[0]['execution_id'], execution_id_3)
        self.assertEqual(res_dict[1]['execution_id'], execution_id_4)
        self.assertEqual(res_dict[2]['execution_id'], execution_id_5)

        ## sort by EXECUTION_ID DESC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'DESC', 'sort_by': 'EXECUTION_ID'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        self.assertEqual(res_dict[0]['execution_id'], execution_id_5)
        self.assertEqual(res_dict[1]['execution_id'], execution_id_4)
        self.assertEqual(res_dict[2]['execution_id'], execution_id_3)

        ## sort by TIME_STARTED ASC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'ASC', 'sort_by': 'TIME_STARTED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        self.assertEqual(res_dict[0]['execution_id'], execution_id_3)
        self.assertEqual(res_dict[1]['execution_id'], execution_id_4)
        self.assertEqual(res_dict[2]['execution_id'], execution_id_5)

        ## sort by TIME_STARTED DESC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'DESC', 'sort_by': 'TIME_STARTED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        self.assertEqual(res_dict[0]['execution_id'], execution_id_5)
        self.assertEqual(res_dict[1]['execution_id'], execution_id_4)
        self.assertEqual(res_dict[2]['execution_id'], execution_id_3)

        ## sort by TIME_COMPLETED ASC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'ASC', 'sort_by': 'TIME_COMPLETED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        self.assertEqual(res_dict[0]['execution_id'], execution_id_3)
        self.assertEqual(res_dict[1]['execution_id'], execution_id_4)
        self.assertEqual(res_dict[2]['execution_id'], execution_id_5)

        ## sort by TIME_COMPLETED DESC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'DESC', 'sort_by': 'TIME_COMPLETED'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        self.assertEqual(res_dict[0]['execution_id'], execution_id_5)
        self.assertEqual(res_dict[1]['execution_id'], execution_id_4)
        self.assertEqual(res_dict[2]['execution_id'], execution_id_3)

        ## sort by VENUE_NAME ASC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'ASC', 'sort_by': 'VENUE_NAME'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        id_1 = res_dict[0]['execution_id']
        id_2 = res_dict[1]['execution_id']
        id_3 = res_dict[2]['execution_id']

        ## sort by VENUE_NAME DESC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'DESC', 'sort_by': 'VENUE_NAME'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        self.assertEqual(res_dict[0]['execution_id'], id_3)
        self.assertEqual(res_dict[1]['execution_id'], id_2)
        self.assertEqual(res_dict[2]['execution_id'], id_1)

        ## sort by STATUS ASC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'ASC', 'sort_by': 'STATUS'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        id_1 = res_dict[0]['execution_id']
        id_2 = res_dict[1]['execution_id']
        id_3 = res_dict[2]['execution_id']

        ## sort by STATUS DESC
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name2, 'sort': 'DESC', 'sort_by': 'STATUS'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions_dict_desc=', json.dumps(executions_dict_desc, indent=4)
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')
        self.assertEqual(res_dict[0]['execution_id'], id_3)
        self.assertEqual(res_dict[1]['execution_id'], id_2)
        self.assertEqual(res_dict[2]['execution_id'], id_1)

        ## Get executions with offset
        url = shared_dict['host'] + '/executions'
        params = {'offset': 1, 'limit': 3}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 3)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)

        logger.debug('result.headers= %s', result.headers)
        self.assertGreater(int(result.headers['x-total-count']), 3)

        self.assertEqual(res_dict[0]['execution_id'], executions_dict[1]['execution_id'])

        ## Get executions with execution_id filter
        url = shared_dict['host'] + '/executions'
        params = {'execution_id': id_1}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['execution_id'], id_1)
        self.assertEqual(result.headers['x-total-count'], '1')
        
        ## Get executions with description filter
        url = shared_dict['host'] + '/executions'
        params = {'description': random_name1}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(result.headers['x-total-count'], '2')

        ## Get executions with description filter. With space in the description.
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name2}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')

        ## Get executions with status filter
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name2, 'status': 'CLOSED'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['execution_id'], execution_id_5)
        self.assertEqual(result.headers['x-total-count'], '1')
        
        ## Get executions with statuses filter
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name2, 'statuses': 'CLOSED'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['execution_id'], execution_id_5)
        self.assertEqual(result.headers['x-total-count'], '1')

        ## Get executions with statuses filter
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name2, 'status': 'IDLE', 'statuses': 'CLOSED'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.headers['x-total-count'], '2')
        res_dict = json.loads(result.text)
        print('executions res_dict=', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 2)
        for execution in res_dict:
            self.assertTrue(execution['status'] in ['IDLE', 'CLOSED'])

        ## Get executions with statuses filter
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name2, 'statuses': 'IDLE,CLOSED'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.headers['x-total-count'], '2')
        res_dict = json.loads(result.text)
        print('executions res_dict=', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 2)
        for execution in res_dict:
            self.assertTrue(execution['status'] in ['IDLE', 'CLOSED'])

        ## Get executions with completed filter: True
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name1, 'completed': 'true'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 1)
        self.assertTrue(res_dict[0]['time_completed'] != '')
        self.assertEqual(result.headers['x-total-count'], '1')

        ## Get executions with completed filter: False
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name1, 'completed': 'false'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertTrue(res_dict[0]['time_completed'] == '')
        self.assertEqual(result.headers['x-total-count'], '1')
        
        ## Get executions with from_time and to_time filters
        url = shared_dict['host'] + '/executions'
        params = {'from_time': time_started_2, 'to_time': time_started_3, 'sort_by': 'EXECUTION_ID', 'sort': 'ASC'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print('executions res_dict=', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(res_dict[0]['execution_id'], execution_id_2)
        self.assertEqual(res_dict[1]['execution_id'], execution_id_3)
        self.assertEqual(result.headers['x-total-count'], '2')        

        ## venue_id filter
        url = shared_dict['host'] + '/executions'
        params = {'venue_id': venue_id_1}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(result.headers['x-total-count'], '1')
        self.assertTrue(res_dict[0]['venue_id'] == venue_id_1)

        ## venue_name filter
        url = shared_dict['host'] + '/executions'
        params = {'venue_name': venue_name_1}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(result.headers['x-total-count'], '1')
        self.assertTrue(res_dict[0]['venue_name'] == venue_name_1)

        ## venue_type filter
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name1, 'venue_type': 'WSTS'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(result.headers['x-total-count'], '2')

        ## venue_type filter (specify a type for which there is no execution)
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name2, 'venue_type': 'Other'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 0)
        self.assertEqual(result.headers['x-total-count'], '0')

        ## Get executions with run_for_score filter: True

        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name2, 'run_for_score': 'true'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        # run_for_score is set when execution is closed
        self.assertEqual(len(res_dict), 0)
        # self.assertTrue(res_dict[0]['run_for_score'] == True)
        self.assertEqual(result.headers['x-total-count'], '0')

        ## Get executions with run_for_score filter: False
        url = shared_dict['host'] + '/executions'
        params = {'description': 'name ' + random_name2, 'run_for_score': 'false'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 3)
        self.assertTrue(res_dict[0]['run_for_score'] == False)
        self.assertTrue(res_dict[1]['run_for_score'] == False)
        self.assertTrue(res_dict[2]['run_for_score'] == False)
        self.assertEqual(result.headers['x-total-count'], '3')

        # test conductor filter
        url = shared_dict['host'] + '/executions'
        params = {'test_conductor': test_conductor_1}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(result.headers['x-total-count'], '2')

        url = shared_dict['host'] + '/executions'
        params = {'test_conductor': test_conductor_2}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 4)
        self.assertEqual(result.headers['x-total-count'], '4')

        # use procedure filter
        url = shared_dict['host'] + '/executions'
        params = {'procedure_id': procedure_id_1}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')

        url = shared_dict['host'] + '/executions'
        params = {'procedure_id': procedure_id_2}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(result.headers['x-total-count'], '2')

        # procedure version filter
        url = shared_dict['host'] + '/executions'
        params = {'procedure_id': procedure_id_2, 'version': 1}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(result.headers['x-total-count'], '2')

        url = shared_dict['host'] + '/executions'
        params = {'procedure_id': procedure_id_2, 'version': 2}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print('executions res_dict=', json.dumps(res_dict, indent=4))
        # print('result.headers=', result.headers)
        self.assertEqual(len(res_dict), 0)
        self.assertEqual(result.headers['x-total-count'], '0')

        # institutional_id filter
        url = shared_dict['host'] + '/executions'
        params = {'institutional_id': institutional_id_1}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 3)
        self.assertEqual(result.headers['x-total-count'], '3')

        url = shared_dict['host'] + '/executions'
        params = {'institutional_id': institutional_id_2}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(result.headers['x-total-count'], '2')

        # institutional_release_id filter
        url = shared_dict['host'] + '/executions'
        params = {'institutional_id': institutional_id_2,
            'institutional_release_id': institutional_release_id_2_1
        }
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(result.headers['x-total-count'], '2')

        url = shared_dict['host'] + '/executions'
        params = {'institutional_id': institutional_id_2,
            'institutional_release_id': 'non_existing_id'
        }
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        # print 'result.headers=', result.headers
        self.assertEqual(len(res_dict), 0)
        self.assertEqual(result.headers['x-total-count'], '0')

        ## Get executions with limit
        url = shared_dict['host'] + '/executions'
        params = {'limit': 3}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        # print 'executions res_dict=', json.dumps(res_dict, indent=4)
        logger.debug('result.headers= %s', result.headers)
        self.assertEqual(len(res_dict), 3)
        self.assertGreater(int(result.headers['x-total-count']), 3)


    def test_create_execution_error(self):
        logger.debug('test_create_execution_error')

        ## Add an execution
        description = 'My new execution'
        res_dict = self.create_execution('venue_id_non_existent', description, 400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)


        #### Create an execution
        venue_id, venue_name = self.create_venue2()
        exe_description = 'My proper execution name ' + random_string(8)
        execution_dict = self.create_execution(venue_id, exe_description)
        execution_id = execution_dict['execution_id']

        ## Try to create another execution for the venue in use.
        ## This works ok since "core" sets venue status, not archive.
        description = 'Another execution for a venue in use'
        res_dict = self.create_execution(venue_id, description)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        # self.assertTrue(len(res_dict['message']) > 0)




    def test_update_execution_elements(self):
        logger.debug('test_update_execution_elements')

        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        ## Try to add an element to a section
        elems_input = [
            {
                'elem_id': section_id_1,
                'title': 'modified title 1'
            },
            {
                'elem_id': step_id_1_1,
                'title': 'modified title 1_1'   
            }
        ]

        id_title_map = {}
        for elem_input in elems_input:
            id_title_map[elem_input['elem_id']] = elem_input['title'] 

        updated_elems = self.update_elements(base_url=execution_url, elems_input=elems_input)
        logger.debug('updated_elems=%s', json.dumps(updated_elems, indent=4))

        self.assertEqual(len(updated_elems), 2)

        for updated_elem in updated_elems:
            self.assertEqual(updated_elem['title'], id_title_map[updated_elem['elem_id']])

    def test_update_procedure_elements(self):
        logger.debug('test_update_procedure_elements')

        id_dict = self.create_procedure_example()
        procedure_id = id_dict['procedure_id']
        procedure_url = id_dict['procedure_url']
        procedure_title = id_dict['procedure_title']
        version = id_dict['version']
        version_description = id_dict['version_description']

        elems = self.get_elements(procedure_url)

        elem_id_1 = elems[0]['elem_id']
        elem_id_2 = elems[1]['elem_id']

        elems_input = [
            {
                'elem_id': elem_id_1,
                'title': 'modified title 1'
            },
            {
                'elem_id': elem_id_2,
                'title': 'modified title 1_1'   
            }
        ]

        id_title_map = {}
        for elem_input in elems_input:
            id_title_map[elem_input['elem_id']] = elem_input['title'] 

        updated_elems = self.update_elements(base_url=procedure_url, elems_input=elems_input)
        logger.debug('updated_elems=%s', json.dumps(updated_elems, indent=4))

        self.assertEqual(len(updated_elems), 2)

        for updated_elem in updated_elems:
            self.assertEqual(updated_elem['title'], id_title_map[updated_elem['elem_id']])

    def test_create_element_error(self):
        logger.debug('test_create_element_error')

        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        # print 'id_dict:', json.dumps(id_dict, indent=4)

        ## Try to add an element to a section
        res_dict = self.add_paragraph(base_url=execution_url,
            insert_after_id=section_id_1,
            level='CHILD',
            description='Paragraph under section 1')

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        paragraph_id = res_dict['elem']['elem_id']

        ## Try to add an element to a step
        res_dict = self.add_paragraph(base_url=execution_url,
            insert_after_id=step_id_3_2,
            level='CHILD',
            description='Paragraph that cannot be added to step',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

        ## Try to add an element to a paragraph
        res_dict = self.add_paragraph(base_url=execution_url,
            insert_after_id=paragraph_id,
            level='CHILD',
            description='Paragraph that cannot be added to paragraph',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

        ## Use insert_after_id that does not belong to execution_id
        venue_id, venue_name = self.create_venue2()
        exe_description = 'My temp execution name ' + random_string(8)
        execution_dict = self.create_execution(venue_id, exe_description)
        execution_id_other = execution_dict['execution_id']

        res_dict = self.add_section(base_url='{0}/executions/{1}'.format(shared_dict['host'], execution_id_other),
            insert_after_id=section_id_1,
            level='CHILD',
            title='Section cannot be added to other execution',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

        ## Use wrong execution_id
        res_dict = self.add_section(base_url='{0}/executions/{1}'.format(shared_dict['host'], 'no_execution_id'),
            insert_after_id=section_id_1,
            level='SIBLING',
            title='Section cannot be added to non existent execution',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

        ## Use wrong insert_after_id
        res_dict = self.add_section(base_url=execution_url,
            insert_after_id='no_id',
            level='SIBLING',
            title='Section that cannot be added',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

        ## Use wrong insert_after_id
        res_dict = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id='not_an_id',
            level='CHILD',
            description='Step that cannot be added',
            guard='',
            variable_name='manual_input_1_2_var',
            code_name='manual_input_step.run',
            code_commit='commit-hash-3dfaea',
            code_release='1.0',
            notices=[],
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

        ## Use wrong insert_after_id
        res_dict = self.add_paragraph(base_url=execution_url,
            insert_after_id='no_id',
            level='SIBLING',
            description='Paragraph that cannot be added',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

    def test_move_element_error(self):
        logger.debug('test_create_element_error')

        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']
        
        # Cannot move to itself
        res_dict = self.move_element(execution_url, section_id_1, section_id_1, 'CHILD', code_expected=400)
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['details']), 1)
        self.assertEqual(res_dict['details'][0], 'Cannot move an element to itself or its child')
                   

        ## Try to move an element as a child of a step
        res_dict = self.move_element(base_url=execution_url,
            elem_id=step_id_3_1,
            insert_after_id=step_id_1_2,
            level='CHILD',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

        ## Try to move an element that does not exist
        res_dict = self.move_element(base_url=execution_url,
            elem_id='not an id',
            insert_after_id=section_id_3,
            level='CHILD',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

        ## Try to move an element to an element that does not exist
        res_dict = self.move_element(base_url=execution_url,
            elem_id=step_id_3_1,
            insert_after_id='not an id',
            level='CHILD',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

        ## Invalid execution id
        res_dict = self.move_element(base_url='{0}/executions/not_an_id'.format(shared_dict['host']),
            elem_id=step_id_3_1,
            insert_after_id=section_id_1,
            level='CHILD',
            code_expected=400)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertTrue(len(res_dict['message']) > 0)

    def test_move_elements(self):
        id_dict = self.create_execution_example()
        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        paragraph_id_2 = id_dict['paragraph_id_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        elements = self.get_elements(execution_url)
        self.assertEqual(len(elements), 7)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_1)
        self.assertEqual(elements[2]['elem_id'], step_id_1_2)
        self.assertEqual(elements[3]['elem_id'], paragraph_id_2)
        self.assertEqual(elements[4]['elem_id'], section_id_3)
        self.assertEqual(elements[5]['elem_id'], step_id_3_1)
        self.assertEqual(elements[6]['elem_id'], step_id_3_2)

        """
        1
          1-1
          1-2
        2
        3
          3-1
          3-2
        """

        ## move element
        res_dict = self.move_elements(execution_url, [section_id_3, paragraph_id_2], step_id_1_1, 'SIBLING')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 5)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], paragraph_id_2)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], section_id_3)
        self.assertEqual(res_dict['numbers'][1]['number'], '1-3')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], step_id_3_1)
        self.assertEqual(res_dict['numbers'][2]['number'], '1-3-1')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], step_id_3_2)
        self.assertEqual(res_dict['numbers'][3]['number'], '1-3-2')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], step_id_1_2)
        self.assertEqual(res_dict['numbers'][4]['number'], '1-4')

        self.assertEqual(len(res_dict['elem_ids']), 7)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)
        self.assertEqual(res_dict['elem_ids'][1], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][2], paragraph_id_2)
        self.assertEqual(res_dict['elem_ids'][3], section_id_3)
        self.assertEqual(res_dict['elem_ids'][4], step_id_3_1)
        self.assertEqual(res_dict['elem_ids'][5], step_id_3_2)
        self.assertEqual(res_dict['elem_ids'][6], step_id_1_2)

        elements = self.get_elements(execution_url)
        logger.debug('after move elements elements= %s', json.dumps(elements, indent=4))   

        self.assertEqual(len(elements), 7)

        for element in elements:
            self.assertEqual(element['execution_id'], execution_id)

        self.assertEqual(elements[0]['number'], '1')
        self.assertEqual(elements[1]['number'], '1-1')
        self.assertEqual(elements[2]['number'], '1-2')
        self.assertEqual(elements[3]['number'], '1-3')
        self.assertEqual(elements[4]['number'], '1-3-1')
        self.assertEqual(elements[5]['number'], '1-3-2')
        self.assertEqual(elements[6]['number'], '1-4')

        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_1)
        self.assertEqual(elements[2]['elem_id'], paragraph_id_2)
        self.assertEqual(elements[3]['elem_id'], section_id_3)
        self.assertEqual(elements[4]['elem_id'], step_id_3_1)
        self.assertEqual(elements[5]['elem_id'], step_id_3_2)
        self.assertEqual(elements[6]['elem_id'], step_id_1_2)

        """
        1
          1-1
          2*
          3*
            3-1*
            3-2*
          1-2*
        """

        # restore
        res_dict = self.move_elements(execution_url, [paragraph_id_2, section_id_3], section_id_1, 'SIBLING')
        logger.debug('move res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 5)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_id_1_2)
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')
        self.assertEqual(res_dict['numbers'][1]['elem_id'], paragraph_id_2)
        self.assertEqual(res_dict['numbers'][1]['number'], '2')
        self.assertEqual(res_dict['numbers'][2]['elem_id'], section_id_3)
        self.assertEqual(res_dict['numbers'][2]['number'], '3')
        self.assertEqual(res_dict['numbers'][3]['elem_id'], step_id_3_1)
        self.assertEqual(res_dict['numbers'][3]['number'], '3-1')
        self.assertEqual(res_dict['numbers'][4]['elem_id'], step_id_3_2)
        self.assertEqual(res_dict['numbers'][4]['number'], '3-2')

        self.assertEqual(len(res_dict['elem_ids']), 7)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)
        self.assertEqual(res_dict['elem_ids'][1], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][2], step_id_1_2)
        self.assertEqual(res_dict['elem_ids'][3], paragraph_id_2)
        self.assertEqual(res_dict['elem_ids'][4], section_id_3)
        self.assertEqual(res_dict['elem_ids'][5], step_id_3_1)
        self.assertEqual(res_dict['elem_ids'][6], step_id_3_2)
        """
        1
          1-1
          1-2*
        2*
        3*
          3-1*
          3-2*
        """





    def test_execution_structure(self):
        logger.debug('test_execution_structure')

        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        ## Add section 1-3
        res_dict = self.add_section(base_url=execution_url,
            insert_after_id=step_id_1_2,
            level='SIBLING',
            title='Section 1-3',
            code_expected=200)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        section_id_1_3 = res_dict['elem']['elem_id']

        res_dict = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=section_id_1_3,
            level='CHILD',
            title='Step 1-3-1',
            guard='',
            variable_name='manual_input_1_2_var',
            code_name='manual_input_step.run',
            code_commit='commit-hash-3dfaea',
            code_release='1.0',
            notices=[])

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        step_id_1_3_1 = res_dict['elem']['elem_id']

        ## Get As Run
        url = shared_dict['host'] + '/executions/' + execution_id + '/as_run'
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('as_run res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(res_dict['children'][0]['title'], 'Section 1')
        self.assertEqual(res_dict['children'][0]['number'], '1')
        self.assertEqual(res_dict['children'][0]['children'][0]['title'], 'Step 1-1')
        self.assertEqual(res_dict['children'][0]['children'][0]['number'], '1-1')
        self.assertEqual(res_dict['children'][0]['children'][1]['title'], 'Step 1-2')
        self.assertEqual(res_dict['children'][0]['children'][1]['number'], '1-2')
        self.assertEqual(res_dict['children'][0]['children'][2]['number'], '1-3')
        self.assertEqual(res_dict['children'][0]['children'][2]['children'][0]['title'], 'Step 1-3-1')
        self.assertEqual(res_dict['children'][0]['children'][2]['children'][0]['number'], '1-3-1')
        self.assertEqual(res_dict['children'][1]['title'], 'Paragraph Section 1')
        self.assertEqual(res_dict['children'][2]['title'], 'Section 3')
        self.assertEqual(res_dict['children'][2]['number'], '3')
        self.assertEqual(res_dict['children'][2]['children'][0]['title'], 'Step 3-1')
        self.assertEqual(res_dict['children'][2]['children'][0]['number'], '3-1')
        self.assertEqual(res_dict['children'][2]['children'][1]['title'], 'Step 3-2')
        self.assertEqual(res_dict['children'][2]['children'][1]['number'], '3-2')

    def test_update_execution(self):
        logger.debug('test_update_execution')
        ## Add a venue
        venue_id, venue_name = self.create_venue2()

        ## Add an execution
        description = 'My new execution'
        execution_dict = self.create_execution(venue_id, description)
        execution_id = execution_dict['execution_id']
        ## Update
        new_description = 'My updated description for this'
        test_conductors = ['hpotter']

        input_dict = {'description': new_description,
            'test_conductors': test_conductors}

        self.update_execution(execution_id, input_dict, code_expected=200)

        # Check
        url = shared_dict['host'] + '/executions/' + execution_id
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        execution_dict_updated = json.loads(result.text)
        logger.debug('execution_dict_updated= %s', json.dumps(execution_dict_updated, indent=4))

        self.assertEqual(execution_dict_updated['description'], new_description)
        self.assertListEqual(execution_dict_updated['test_conductors'], test_conductors)

    def test_step_result(self):
        logger.debug('test_step_result')

        ## Add a venue
        venue_id, venue_name = self.create_venue2()

        ## Add an execution
        description = 'My execution with results'
        execution_dict = self.create_execution(venue_id, description)
        execution_id = execution_dict['execution_id']
        execution_url = shared_dict['host'] + '/executions/' + execution_id

        ## Add section 1
        res_dict = self.add_section(base_url=execution_url,
            insert_after_id='-1',
            level='',
            title='Section 1')

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        section_id_1 = res_dict['elem']['elem_id']
        self.assertEqual(res_dict['elem']['number'], '1')

        ## Add step 1-1
        res_dict = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=section_id_1,
            level='CHILD',
            description='Step 1-1',
            guard='',
            variable_name='manual_input_1_1_var',
            code_name='manual_input_step.run',
            code_commit='commit-hash-3dfaea',
            code_release='1.0',
            notices=[])

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        step_id_1_1 = res_dict['elem']['elem_id']
        self.assertEqual(res_dict['elem']['number'], '1-1')

        self.update_element(execution_url, step_id_1_1, {'executable': 'EXECUTED'})

        ## Add step 1-2
        res_dict = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=step_id_1_1,
            level='SIBLING',
            description='Step 1-2',
            guard='',
            variable_name='manual_input_1_2_var',
            code_name='manual_input_step.run',
            code_commit='commit-hash-3dfaea',
            code_release='1.0',
            notices=[])

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        step_id_1_2 = res_dict['elem']['elem_id']
        self.assertEqual(res_dict['elem']['number'], '1-2')

        self.update_element(execution_url, step_id_1_2, {'executable': 'EXECUTED'})

        # Set user input
        user_input_1_1_first = {
            'entries': [
                {
                    'name': 'var1',
                    'type': 'FLOAT',
                    'verification_condition': 'RECORD',
                    'verification_values': [],
                    'actual_value': 11.0
                },
                {
                    'name': 'var2',
                    'type': 'STRING',
                    'verification_condition': 'RECORD',
                    'verification_values': [],
                    'actual_value': 'abc'
                }
            ]
        }
        self.set_step_input_generic(base_url=execution_url, elem_id=step_id_1_1,
            user_input=user_input_1_1_first)

        # Get user input
        user_input_actual = self.get_step_input_generic(base_url=execution_url, elem_id=step_id_1_1)
        logger.debug('user_input_actual= %s', json.dumps(user_input_actual, indent=4))

        self.assertDictEqual(user_input_1_1_first, user_input_actual)

        # Set result
        step_result_1_1_first = {
            'meta_data': {
                'test_conductor': 'Homer Simpson', 
                'status': 'PASS',
                'error': {},
                'status_message': '',
                'time_completed': '2020-12-05T00:42:22.503Z',
                'time_started': '2020-12-05T00:42:11.832Z',
                'time_updated': '2020-12-05T00:42:22.503Z'
            },
            'results': {
                'entries': [
                    {
                        'name': 'var1',
                        'type': 'FLOAT',
                        'verification_condition': 'RECORD',
                        'verification_values': [],
                        'actual_value': 11.0,
                        'verification_status': 'PASS'
                    },
                    {
                        'name': 'var2',
                        'type': 'STRING',
                        'verification_condition': 'RECORD',
                        'verification_values': [],
                        'actual_value': 'abc',
                        'verification_status': 'PASS'
                    }
                ]
            }
        }
        step_actual = self.set_step_output_generic(base_url=execution_url, elem_id=step_id_1_1,
            output=step_result_1_1_first, code_expected=200)
        logger.debug('step_actual= %s', json.dumps(step_actual, indent=4))
        self.assertDictEqual(step_result_1_1_first, step_actual['execution'])

        # Get step output
        step_result_actual = self.get_step_output_generic(base_url=execution_url, elem_id=step_id_1_1)
        logger.debug('step_result_actual= %s', json.dumps(step_result_actual, indent=4))

        self.assertDictEqual(step_result_1_1_first, step_result_actual)

        res_dict = self.get_history(execution_id)
        logger.debug('history res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 1)        

        ## set results one more time without creating a new run. This should not create execution record.
        step_actual = self.set_step_output_generic(base_url=execution_url, elem_id=step_id_1_1,
            output=step_result_1_1_first, code_expected=200)
        logger.debug('step_actual= %s', json.dumps(step_actual, indent=4))
        self.assertDictEqual(step_result_1_1_first, step_actual['execution'])

        res_dict = self.get_history(execution_id)
        logger.debug('history res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 1)       

        elements = self.get_elements(execution_url)

        logger.debug('elements= %s', json.dumps(elements, indent=4))  

        self.assertEqual(len(elements[1]['run_records']), 0)

        # Now, create a new run

        res_dict = self.create_new_run(execution_id=execution_id, elem_id=step_id_1_1)
        logger.debug('create_new_run res_dict= %s', json.dumps(res_dict, indent=4))
        
        self.assertEqual(res_dict.get('_id'), None) 
        self.assertEqual(res_dict.get('_key'), None)
        self.assertEqual(res_dict.get('_rev'), None)

        self.assertEqual(len(res_dict['run_records']), 1)
        self.assertEqual(res_dict['run_records'][0].get('run_records'), None)
        self.assertEqual(res_dict['run_records'][0].get('_id'), None) 
        self.assertEqual(res_dict['run_records'][0].get('_key'), None)
        self.assertEqual(res_dict['run_records'][0].get('_rev'), None) 

        self.assertEqual(res_dict['execution']['meta_data']['test_conductor'], '') 
        # This check does not work since specification is not provided in this test
        # self.assertEqual(len(res_dict['execution']['results']['entries']), 0)      

        # Set user input
        user_input_1_1 = {
            'entries': [
                {
                    'name': 'var1',
                    'type': 'FLOAT',
                    'verification_condition': 'RECORD',
                    'verification_values': [],
                    'actual_value': 12.0
                },
                {
                    'name': 'var2',
                    'type': 'STRING',
                    'verification_condition': 'RECORD',
                    'verification_values': [],
                    'actual_value': 'abcd'
                }
            ]
        }
        self.set_step_input_generic(base_url=execution_url, elem_id=step_id_1_1,
            user_input=user_input_1_1)

        # Get user input
        user_input_actual = self.get_step_input_generic(base_url=execution_url, elem_id=step_id_1_1)
        logger.debug('user_input_actual= %s', json.dumps(user_input_actual, indent=4))

        self.assertDictEqual(user_input_1_1, user_input_actual)

        # Set result
        step_result_1_1 = {
            'meta_data': {
                'error': {},
                'status': 'PASS',
                'status_message': '',
                'test_conductor': 'Homer Simpson',
                'time_completed': '2020-12-05T00:43:22.503Z',
                'time_started': '2020-12-05T00:43:11.832Z',
                'time_updated': '2020-12-05T00:43:22.503Z',
                'override_justification': '',
                'overridden_by': '',
                'time_overridden': ''
            },            
            'results': {
                'entries': [
                    {
                        'name': 'var1',
                        'type': 'FLOAT',
                        'verification_condition': 'RECORD',
                        'verification_values': [],
                        'actual_value': 12.0,
                        'verification_status': 'PASS'
                    },
                    {
                        'name': 'var2',
                        'type': 'STRING',
                        'verification_condition': 'RECORD',
                        'verification_values': [],
                        'actual_value': 'abcd',
                        'verification_status': 'PASS'
                    }
                ]
            }
        }
        self.set_step_output_generic(base_url=execution_url, elem_id=step_id_1_1,
            output=step_result_1_1, code_expected=200)

        # Get step output
        step_result_actual = self.get_step_output_generic(base_url=execution_url, elem_id=step_id_1_1)
        logger.debug('step_result_actual= %s', json.dumps(step_result_actual, indent=4))

        self.assertDictEqual(step_result_1_1, step_result_actual)

        # Get step with input and result
        step_actual = self.get_step_generic(base_url=execution_url, elem_id=step_id_1_1)
        logger.debug('step_actual= %s', json.dumps(step_actual, indent=4))

        self.assertDictEqual(step_actual['execution_user_input'], user_input_1_1)
        self.assertDictEqual(step_actual['execution'], step_result_1_1)

        # Set user input for step 1-2
        user_input_1_2 = {
            'entries': [
                {
                    'name': 'var1',
                    'type': 'FLOAT',
                    'verification_condition': 'RECORD',
                    'verification_values': [],
                    'actual_value': 21.0
                },
                {
                    'name': 'var2',
                    'type': 'STRING',
                    'verification_condition': 'RECORD',
                    'verification_values': [],
                    'actual_value': 'ABC'
                }
            ]
        }
        self.set_step_input_generic(base_url=execution_url, elem_id=step_id_1_2,
            user_input=user_input_1_2)

        # Get user input
        user_input_actual = self.get_step_input_generic(base_url=execution_url, elem_id=step_id_1_2)
        logger.debug('user_input_actual= %s', json.dumps(user_input_actual, indent=4))
        self.assertDictEqual(user_input_actual, user_input_1_2)

        # Set result for step 1-2
        step_result_1_2 = {
            'meta_data': {
                'test_conductor': 'Homer Simpson', 
                'status': 'PASS',
                'time_completed': '2020-12-05T00:45:22.503Z',
                'time_started': '2020-12-05T00:45:11.832Z',
                'time_updated': '2020-12-05T00:45:22.503Z'
            },
            'results': {
                'entries': [
                    {
                        'name': 'var1',
                        'type': 'FLOAT',
                        'verification_condition': 'RECORD',
                        'verification_values': [],
                        'actual_value': 21.0,
                        'verification_status': 'PASS'
                    },
                    {
                        'name': 'var2',
                        'type': 'STRING',
                        'verification_condition': 'RECORD',
                        'verification_values': [],
                        'actual_value': 'ABC',
                        'verification_status': 'PASS'
                    }
                ]
            }
        }
        self.set_step_output_generic(base_url=execution_url, elem_id=step_id_1_2,
            output=step_result_1_2, code_expected=200)

        # Get step output
        step_result_actual = self.get_step_output_generic(base_url=execution_url, elem_id=step_id_1_2)
        logger.debug('step_result_actual= %s', json.dumps(step_result_actual, indent=4))
        self.assertDictEqual(step_result_actual, step_result_1_2)

        # check as run
        res_dict = self.get_as_run(execution_id)
        logger.debug('as_run res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertDictEqual(res_dict['children'][0]['children'][0]['execution_user_input'], user_input_1_1)
        self.assertDictEqual(res_dict['children'][0]['children'][0]['execution'], step_result_1_1)
        self.assertEqual(res_dict['children'][0]['children'][0]['executed'], True)

        self.assertDictEqual(res_dict['children'][0]['children'][1]['execution_user_input'], user_input_1_2)
        self.assertDictEqual(res_dict['children'][0]['children'][1]['execution'], step_result_1_2)
        self.assertEqual(res_dict['children'][0]['children'][1]['executed'], True)

        # check elements
        res_dict = self.get_elements(execution_url)
        logger.debug('elements res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 3)
        self.assertEqual(len(res_dict[1]['run_records']), 1)
        self.assertEqual(res_dict[1]['run_records'][0].get('run_records'), None)
        self.assertEqual(res_dict[1]['run_records'][0].get('_id'), None) 
        self.assertEqual(res_dict[1]['run_records'][0].get('_key'), None)
        self.assertEqual(res_dict[1]['run_records'][0].get('_rev'), None)          

        # check history
        res_dict = self.get_history(execution_id)
        logger.debug('history res_dict= %s', json.dumps(res_dict, indent=4))

        self.assertEqual(len(res_dict), 3)

        # previous execution record is stored as a new element with a different elem_id
        # self.assertEqual(res_dict[0]['elem_id'], step_id_1_1)
        self.assertDictEqual(res_dict[0]['execution'], step_result_1_1_first)
        
        # previous execution record is stored as a new element with a different elem_id
        # self.assertEqual(res_dict[1]['elem_id'], step_id_1_1)
        self.assertDictEqual(res_dict[1]['execution'], step_result_1_1)

        self.assertEqual(res_dict[2]['elem_id'], step_id_1_2)
        self.assertDictEqual(res_dict[2]['execution'], step_result_1_2)
   

    def run_get_elements(self, execution_id):
        # Get elements
        url = shared_dict['host'] + '/executions/' + execution_id + '/elements'
        result = requests.get(url, headers=shared_dict['headers'])
        logger.debug('url=%s', result.url)
        self.assertEqual(result.status_code, 200)
        elems = json.loads(result.text)
        logger.debug('elems= %s', json.dumps(elems, indent=4))
        logger.debug('x-total-count= %s', result.headers['x-total-count'])
        self.assertEqual(result.headers['x-total-count'], '7')
        self.assertEqual(len(elems), 7)
        self.assertEqual(elems[0]['number'], "1")
        self.assertEqual(elems[1]['number'], "1-1")
        self.assertEqual(elems[2]['number'], "1-2")
        self.assertEqual(elems[3]['number'], "2")
        self.assertEqual(elems[4]['number'], "3")
        self.assertEqual(elems[5]['number'], "3-1")
        self.assertEqual(elems[6]['number'], "3-2")

        # Get simple elements
        url = shared_dict['host'] + '/executions/' + execution_id + '/simple_elements'
        result = requests.get(url, headers=shared_dict['headers'])
        logger.debug('url=%s', result.url)
        logger.debug('result.text=%s', result.text)
        self.assertEqual(result.status_code, 200)
        simple_elems = json.loads(result.text)
        logger.debug('simple_elems= %s', json.dumps(simple_elems, indent=4))
        logger.debug('x-total-count= %s', result.headers['x-total-count'])

        self.assertEqual(result.headers['x-total-count'], '7')
        self.assertEqual(len(elems), 7)
        for i in range(7):
            self.assertEqual(simple_elems[i]['elem_id'], elems[i]['elem_id'])
            self.assertEqual(simple_elems[i]['elem_type'], elems[i]['elem_type'])
            self.assertEqual(simple_elems[i]['executable'], elems[i]['executable'])
            self.assertEqual(simple_elems[i]['number'],  elems[i]['number'])

        # description filter
        url = shared_dict['host'] + '/executions/' + execution_id + '/elements'
        params = {'description': 'TIO'}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        elems = json.loads(result.text)
        self.assertEqual(result.headers['x-total-count'], '1')
        self.assertEqual(len(elems), 1)
        logger.debug('elems= %s', json.dumps(elems, indent=4))

        # Get steps
        url = shared_dict['host'] + '/executions/' + execution_id + '/steps'
        result = requests.get(url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        steps = json.loads(result.text)
        logger.debug('steps= %s', json.dumps(steps, indent=4))
        logger.debug('x-total-count= %s', result.headers['x-total-count'])
        self.assertEqual(result.headers['x-total-count'], '4')
        self.assertEqual(len(steps), 4)

        for step in steps:
            self.assertEqual(step['elem_type'], 'STEP')

        # filters
        url = shared_dict['host'] + '/executions/' + execution_id + '/steps'
        params = {'offset': 1, 'limit': 2}
        result = requests.get(url, params = params, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        steps = json.loads(result.text)
        logger.debug('steps= %s', json.dumps(steps, indent=4))
        logger.debug('x-total-count= %s', result.headers['x-total-count'])
        self.assertEqual(result.headers['x-total-count'], '4')
        self.assertEqual(len(steps), 2)

        for step in steps:
            self.assertEqual(step['elem_type'], 'STEP')

        # Get sections
        url = shared_dict['host'] + '/executions/' + execution_id + '/elements'
        params = {'elem_type': 'SECTION'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        # print 'url=', result.url
        self.assertEqual(result.status_code, 200)
        sections = json.loads(result.text)
        logger.debug('sections= %s', json.dumps(sections, indent=4))
        logger.debug('x-total-count= %s', result.headers['x-total-count'])
        self.assertEqual(result.headers['x-total-count'], '2')
        self.assertEqual(len(sections), 2)

        for section in sections:
            self.assertEqual(section['elem_type'], 'SECTION')

        # Get sections
        url = shared_dict['host'] + '/executions/' + execution_id + '/sections'
        result = requests.get(url, headers=shared_dict['headers'])
        # print 'url=', result.url
        self.assertEqual(result.status_code, 200)
        sections = json.loads(result.text)
        logger.debug('sections= %s', json.dumps(sections, indent=4))
        logger.debug('x-total-count= %s', result.headers['x-total-count'])
        self.assertEqual(result.headers['x-total-count'], '2')
        self.assertEqual(len(sections), 2)

        for section in sections:
            self.assertEqual(section['elem_type'], 'SECTION')

        # Get paragraphs
        url = shared_dict['host'] + '/executions/' + execution_id + '/elements'
        params = {'elem_type': 'PARAGRAPH'}
        result = requests.get(url, params=params, headers=shared_dict['headers'])
        # print 'url=', result.url
        self.assertEqual(result.status_code, 200)
        paragraphs = json.loads(result.text)
        logger.debug('paragraph= %s', json.dumps(paragraphs, indent=4))
        logger.debug('x-total-count= %s', result.headers['x-total-count'])
        self.assertEqual(result.headers['x-total-count'], '1')
        self.assertEqual(len(paragraphs), 1)

        for paragraph in paragraphs:
            self.assertEqual(paragraph['elem_type'], 'PARAGRAPH')

        # Get paragraphs
        url = shared_dict['host'] + '/executions/' + execution_id + '/paragraphs'
        result = requests.get(url, headers=shared_dict['headers'])
        # print 'url=', result.url
        self.assertEqual(result.status_code, 200)
        paragraphs = json.loads(result.text)
        logger.debug('paragraph= %s', json.dumps(paragraphs, indent=4))
        logger.debug('x-total-count= %s', result.headers['x-total-count'])
        self.assertEqual(result.headers['x-total-count'], '1')
        self.assertEqual(len(paragraphs), 1)

        for paragraph in paragraphs:
            self.assertEqual(paragraph['elem_type'], 'PARAGRAPH')

    def test_next_element(self):
        logger.debug('test_next_element')

        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        paragraph_id_2 = id_dict['paragraph_id_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        elem = self.get_next_element(execution_url, section_id_1, True)
        self.assertEqual(elem['elem_id'], step_id_1_1)

        elem = self.get_next_element(execution_url, step_id_1_1, True)
        self.assertEqual(elem['elem_id'], step_id_1_2)        

        elem = self.get_next_element(execution_url, step_id_1_2, True)
        self.assertEqual(elem['elem_id'], step_id_3_1)  

        elem = self.get_next_element(execution_url, paragraph_id_2, False)
        self.assertEqual(elem['elem_id'], section_id_3)  

        elem = self.get_next_element(execution_url, section_id_3, False)
        self.assertEqual(elem['elem_id'], step_id_3_1)          

    @unittest.skip("Run only to delete all executions.")
    def test_delete_executions(self):
        logger.debug('test_delete_executions')
        ## Get list of executions
        url = shared_dict['host'] + '/executions'
        result = requests.get(url,
            headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        logger.debug('number of executions= %s', len(res_dict))

        for execution in res_dict:
            url = shared_dict['host'] + '/executions/' + execution['execution_id']
            logger.debug('DELETE url= %s', url)
            result = requests.delete(url,
                headers=shared_dict['headers'])
            logger.debug('result.status_code= %s', result.status_code)
            self.assertEqual(result.status_code, 204)

    def test_delete_execution(self):
        logger.debug('test_delete_execution')

        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        if False:
            self.delete_element(execution_url, section_id_1)
        if False:
            self.delete_element(execution_url, step_id_1_2)
        if False:
            res_dict = self.move_element(base_url=execution_url,
            elem_id=step_id_1_1, insert_after_id=section_id_3, level='CHILD')

        # Set user input
        execution_user_input = {
            'temperature': {
                'verification_condition': 'RECORD',
                'verification_values': [],
                'actual_value': 21.0
            },
            'humidity': {
                'verification_condition': 'RECORD',
                'verification_values': [],
                'actual_value': 41.0
            }
        }
        self.set_step_input_generic(base_url=execution_url, elem_id=step_id_1_1,
            user_input=execution_user_input)

        # Set result
        step_result = {
            'meta_data': {'test_conductor': 'Homer Simpson'},
            'results': {
                'temperature': {
                    'verification_condition': 'RECORD',
                    'verification_values': [],
                    'actual_value': 21.0,
                    'verification_status': 'PASS'
                },
                'humidity': {
                    'verification_condition': 'RECORD',
                    'verification_values': [],
                    'actual_value': 41.0,
                    'verification_status': 'PASS'
                }
            }
        }
        self.set_step_output_generic(base_url=execution_url, elem_id=step_id_1_1,
            output=step_result, code_expected=200)

        # now delete the execution

        url = '{0}/executions/{1}'.format(shared_dict['host'], execution_id)
        logger.debug('DELETE url= %s', url)
        result = requests.delete(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 204)

    def test_steps(self):
        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        url = '{0}/executions/{1}/steps/{2}'.format(shared_dict['host'], execution_id, step_id_1_1)
        result = requests.get(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['elem_id'], step_id_1_1)

        url = '{0}/executions/{1}/steps/{2}'.format(shared_dict['host'], execution_id, step_id_1_1)
        new_description = 'new description'
        step_dict = {'description': new_description}
        result = requests.patch(url,
            headers=shared_dict['headers'],
            data=json.dumps(step_dict))
        logger.debug('result.status_code= %s', result.status_code)
        self.assertEqual(result.status_code, 200)

        url = '{0}/executions/{1}/steps/{2}'.format(shared_dict['host'], execution_id, step_id_1_1)
        result = requests.get(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['elem_id'], step_id_1_1)
        self.assertEqual(res_dict['description'], new_description)

        url = '{0}/executions/{1}/elements/{2}'.format(shared_dict['host'], execution_id, step_id_1_1)
        step_dict = {'description': new_description}
        result = requests.delete(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 1)


    def test_sections(self):
        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        url = '{0}/executions/{1}/sections/{2}'.format(shared_dict['host'], execution_id, section_id_1)
        result = requests.get(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['elem_id'], section_id_1)

        url = '{0}/executions/{1}/sections/{2}'.format(shared_dict['host'], execution_id, section_id_1)
        new_description = 'new description'
        step_dict = {'description': new_description}
        result = requests.patch(url,
            headers=shared_dict['headers'],
            data=json.dumps(step_dict))
        logger.debug('result.status_code= %s', result.status_code)
        self.assertEqual(result.status_code, 200)

        url = '{0}/executions/{1}/sections/{2}'.format(shared_dict['host'], execution_id, section_id_1)
        result = requests.get(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['elem_id'], section_id_1)
        self.assertEqual(res_dict['description'], new_description)

        url = '{0}/executions/{1}/elements/{2}'.format(shared_dict['host'], execution_id, section_id_1)
        step_dict = {'description': new_description}
        result = requests.delete(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 4)

    def test_paragraphs(self):
        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']
        paragraph_id_2 = id_dict['paragraph_id_2']

        url = '{0}/executions/{1}/paragraphs/{2}'.format(shared_dict['host'], execution_id, paragraph_id_2)
        result = requests.get(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['elem_id'], paragraph_id_2)

        url = '{0}/executions/{1}/paragraphs/{2}'.format(shared_dict['host'], execution_id, paragraph_id_2)
        new_description = 'new description'
        step_dict = {'description': new_description}
        result = requests.patch(url,
            headers=shared_dict['headers'],
            data=json.dumps(step_dict))
        logger.debug('result.status_code= %s', result.status_code)
        self.assertEqual(result.status_code, 200)

        url = '{0}/executions/{1}/paragraphs/{2}'.format(shared_dict['host'], execution_id, paragraph_id_2)
        result = requests.get(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        logger.debug('result.text= %s', result.text)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['elem_id'], paragraph_id_2)
        self.assertEqual(res_dict['description'], new_description)

        url = '{0}/executions/{1}/elements/{2}'.format(shared_dict['host'], execution_id, paragraph_id_2)
        step_dict = {'description': new_description}
        result = requests.delete(url,
            headers=shared_dict['headers'])
        logger.debug('result.status_code= %s', result.status_code)
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertEqual(len(res_dict['numbers']), 3)

    def test_comments(self):
        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']

        # Add comment to section
        content1 = 'This is the first comment for the section'
        res_dict = self.add_conversation(execution_url, section_id_1, {'type': 'DATA_REVIEW_COMMENT'})
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
        execution = self.get_execution(execution_id)
        self.assertEqual(execution['comment_conversations_count'], 0)
        self.assertEqual(execution['unresolved_comment_conversations_count'], 0)
        self.assertEqual(execution['ar_conversations_count'], 0)
        self.assertEqual(execution['unresolved_ar_conversations_count'], 0)
        self.assertEqual(execution['dr_conversations_count'], 1)
        self.assertEqual(execution['unresolved_dr_conversations_count'], 1)
        self.assertEqual(execution['conversations_count'], 1)
        self.assertEqual(execution['unresolved_conversations_count'], 1)
        
        res_dict = self.update_comment(execution_url, section_id_1, conversation_id_1, comment_id_1, content1)
        self.assertEqual(res_dict['content'], content1)
        
        time.sleep(0.01)

        # update comment
        content1b = 'This is the first comment for the section and updated'

        res_dict = self.update_comment(execution_url, section_id_1, conversation_id_1, comment_id_1, content1b)

        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['content'], content1b)        
        time_updated_1b = res_dict['time_updated']      
        self.assertGreater(time_updated_1b, time_updated_1)   
        self.assertTrue(len(res_dict['user_name']) > 0)        

        # set it back
        res_dict = self.update_comment(execution_url, section_id_1, conversation_id_1, comment_id_1, content1)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['content'], content1)                   

        # check the section
        section_dict = self.get_section(execution_url, section_id_1)
        self.assertEqual(len(section_dict['conversations']), 1)
        self.assertEqual(len(section_dict['conversations'][0]['comments']), 1)
        self.assertEqual(section_dict['conversations'][0]['comments'][0]['content'], content1)

        # Add another comment to section
        content2 = 'This is the second comment for the section'
        res_dict = self.add_comment(execution_url, section_id_1, conversation_id_1, content2)
        comment_id_2 = res_dict['comment_id']
        self.assertEqual(res_dict['content'], content2)

        # check the section
        section_dict = self.get_section(execution_url, section_id_1)
        self.assertEqual(len(section_dict['conversations']), 1)
        self.assertEqual(len(section_dict['conversations'][0]['comments']), 2)        
        self.assertEqual(section_dict['conversations'][0]['comments'][0]['content'], content1)
        self.assertEqual(section_dict['conversations'][0]['comments'][1]['content'], content2)

        # get comments
        comments_dict = self.get_comments(execution_url, section_id_1, conversation_id_1)
        self.assertEqual(len(comments_dict), 2)
        self.assertEqual(comments_dict[0]['content'], content1)
        self.assertEqual(comments_dict[1]['content'], content2)

        # get comment
        comment1_dict = self.get_comment(execution_url, section_id_1, conversation_id_1, comment_id_1)
        self.assertEqual(comment1_dict['content'], content1)

        # get comment
        comment2_dict = self.get_comment(execution_url, section_id_1, conversation_id_1, comment_id_2)
        self.assertEqual(comment2_dict['content'], content2)

        # delete comment
        self.delete_comment(execution_url, section_id_1, conversation_id_1, comment_id_1)

        # delete a non-existing comment
        self.delete_comment(execution_url, 'not_an_elem_id', conversation_id_1, 'not_a_comment_id', 400)

        # delete a non-existing comment
        self.delete_comment(execution_url, section_id_1, conversation_id_1, 'not_a_comment_id', 400)

        # get comments
        comments_dict = self.get_comments(execution_url, section_id_1, conversation_id_1)
        logger.debug('comments_dict: %s', json.dumps(comments_dict, indent=4))
        self.assertEqual(len(comments_dict), 1)
        self.assertEqual(comments_dict[0]['content'], content2)
        
        # add another conversation
        content_2_1 = 'This is the first comment of the second conversation'
        res_dict = self.add_conversation(execution_url, section_id_1, {'type': 'COMMENT'})
        conversation_id_2 = res_dict['conversation_id']
        comment_2_1 = res_dict['comments'][0]
        comment_id_2_1 = comment_2_1['comment_id']        
         
        res_dict = self.update_comment(execution_url, section_id_1, conversation_id_2, comment_id_2_1, content_2_1)
        self.assertEqual(res_dict['content'], content_2_1)         

        # check conversations count
        execution = self.get_execution(execution_id)
        self.assertEqual(execution['comment_conversations_count'], 1)
        self.assertEqual(execution['unresolved_comment_conversations_count'], 1)
        self.assertEqual(execution['ar_conversations_count'], 0)
        self.assertEqual(execution['unresolved_ar_conversations_count'], 0)
        self.assertEqual(execution['dr_conversations_count'], 1)
        self.assertEqual(execution['unresolved_dr_conversations_count'], 1)
        self.assertEqual(execution['conversations_count'], 2)
        self.assertEqual(execution['unresolved_conversations_count'], 2)
        
        # add another comment
        content_2_2 = 'This is the second comment of the second conversation'
        res_dict = self.add_comment(execution_url, section_id_1, conversation_id_2, content_2_2)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        comment_id_2_2 = res_dict['comment_id']
        self.assertEqual(res_dict['content'], content_2_2)
        
        # get conversations
        res_dict = self.get_conversations(execution_url, section_id_1)
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(len(res_dict[1]['comments']), 2)
        self.assertEqual(res_dict[1]['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict[1]['comments'][1]['content'], content_2_2)
        
        # get conversation
        res_dict = self.get_conversation(execution_url, section_id_1, conversation_id_2)
        self.assertEqual(len(res_dict['comments']), 2)
        self.assertEqual(res_dict['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict['comments'][1]['content'], content_2_2)     
        self.assertEqual(res_dict['status'], 'UNRESOLVED') 
        self.assertEqual(res_dict['time_resolved'], '')
        self.assertEqual(res_dict['resolved_by'], '')
        
        # resolve conversation
        res_dict = self.update_conversation(execution_url, section_id_1, conversation_id_2, {'status': 'RESOLVED'})
        # check conversation
        res_dict = self.get_conversation(execution_url, section_id_1, conversation_id_2)
        self.assertEqual(len(res_dict['comments']), 2)
        self.assertEqual(res_dict['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict['comments'][1]['content'], content_2_2)     
        self.assertEqual(res_dict['status'], 'RESOLVED') 
        self.assertTrue(len(res_dict['time_resolved']) > 0)
        self.assertTrue(len(res_dict['resolved_by']) > 0) 

        # check conversations count
        execution = self.get_execution(execution_id)
        self.assertEqual(execution['comment_conversations_count'], 1)
        self.assertEqual(execution['unresolved_comment_conversations_count'], 0)
        self.assertEqual(execution['ar_conversations_count'], 0)
        self.assertEqual(execution['unresolved_ar_conversations_count'], 0)
        self.assertEqual(execution['dr_conversations_count'], 1)
        self.assertEqual(execution['unresolved_dr_conversations_count'], 1)
        self.assertEqual(execution['conversations_count'], 2)
        self.assertEqual(execution['unresolved_conversations_count'], 1)
        
        # unresolve conversation
        res_dict = self.update_conversation(execution_url, section_id_1, conversation_id_2, {'status': 'UNRESOLVED'})
        # check conversation
        res_dict = self.get_conversation(execution_url, section_id_1, conversation_id_2)
        self.assertEqual(len(res_dict['comments']), 2)
        self.assertEqual(res_dict['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict['comments'][1]['content'], content_2_2)     
        self.assertEqual(res_dict['status'], 'UNRESOLVED') 
        self.assertEqual(res_dict['time_resolved'], '')
        self.assertEqual(res_dict['resolved_by'], '')
        
        # check conversations count
        execution = self.get_execution(execution_id)
        self.assertEqual(execution['comment_conversations_count'], 1)
        self.assertEqual(execution['unresolved_comment_conversations_count'], 1)
        self.assertEqual(execution['ar_conversations_count'], 0)
        self.assertEqual(execution['unresolved_ar_conversations_count'], 0)
        self.assertEqual(execution['dr_conversations_count'], 1)
        self.assertEqual(execution['unresolved_dr_conversations_count'], 1)
        self.assertEqual(execution['conversations_count'], 2)
        self.assertEqual(execution['unresolved_conversations_count'], 2)

        # delete conversation
        res_dict = self.delete_conversation(execution_url, section_id_1, conversation_id_1)
        
        # check conversations
        res_dict = self.get_conversations(execution_url, section_id_1)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(len(res_dict[0]['comments']), 2)
        self.assertEqual(res_dict[0]['comments'][0]['content'], content_2_1)
        self.assertEqual(res_dict[0]['comments'][1]['content'], content_2_2)

        # check conversations count
        execution = self.get_execution(execution_id)
        self.assertEqual(execution['comment_conversations_count'], 1)
        self.assertEqual(execution['unresolved_comment_conversations_count'], 1)
        self.assertEqual(execution['ar_conversations_count'], 0)
        self.assertEqual(execution['unresolved_ar_conversations_count'], 0)
        self.assertEqual(execution['dr_conversations_count'], 0)
        self.assertEqual(execution['unresolved_dr_conversations_count'], 0)
        self.assertEqual(execution['conversations_count'], 1)
        self.assertEqual(execution['unresolved_conversations_count'], 1)
   
    def test_comments_filter(self):
        
        id_dict = self.create_execution_example()
        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']
        step_id_1_2 = id_dict['step_id_1_2']
        paragraph_id_2 = id_dict['paragraph_id_2']
        section_id_3 = id_dict['section_id_3']
        step_id_3_1 = id_dict['step_id_3_1']
        step_id_3_2 = id_dict['step_id_3_2']
        
        outline_elems = self.get_execution_outline(execution_url)
        # logger.debug('outline_elems: %s', json.dumps(outline_elems, indent=4))
        self.assertEqual(len(outline_elems), 7)        
        self.assertEqual(outline_elems[0]['elem_id'], section_id_1)
        self.assertEqual(outline_elems[1]['elem_id'], step_id_1_1)
        self.assertEqual(outline_elems[2]['elem_id'], step_id_1_2)   
        self.assertEqual(outline_elems[3]['elem_id'], paragraph_id_2) 
        self.assertEqual(outline_elems[4]['elem_id'], section_id_3)
        self.assertEqual(outline_elems[5]['elem_id'], step_id_3_1)
        self.assertEqual(outline_elems[6]['elem_id'], step_id_3_2)
        
        elements = self.get_elements(execution_url)
        # logger.debug('elements res_dict= %s', json.dumps(elements, indent=4))
        
        res_dict = self.add_conversation(execution_url, step_id_1_1, {'type': 'COMMENT'})
        res_dict = self.add_conversation(execution_url, section_id_3, {'type': 'COMMENT'})
        res_dict = self.add_conversation(execution_url, step_id_3_1, {'type': 'COMMENT'})
        
        elements = self.get_elements(execution_url, params={'comment_filter': 'ON'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0]['elem_id'], step_id_1_1)
        self.assertEqual(elements[1]['elem_id'], section_id_3)
        self.assertEqual(elements[2]['elem_id'], step_id_3_1)     
        
        elements = self.get_elements(execution_url, params={'comment_filter': 'OFF'})
        logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 7)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_1)
        self.assertEqual(elements[2]['elem_id'], step_id_1_2)   
        self.assertEqual(elements[3]['elem_id'], paragraph_id_2) 
        self.assertEqual(elements[4]['elem_id'], section_id_3)
        self.assertEqual(elements[5]['elem_id'], step_id_3_1)
        self.assertEqual(elements[6]['elem_id'], step_id_3_2)              
        
        elements = self.get_elements(execution_url, params={'comment_filter': 'ON', 'limit': 2})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], step_id_1_1)
        self.assertEqual(elements[1]['elem_id'], section_id_3)          
        
        elements = self.get_elements(execution_url, params={'comment_filter': 'ON', 'offset': 1, 'limit': 2})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], section_id_3)
        self.assertEqual(elements[1]['elem_id'], step_id_3_1)    
        
        elements = self.get_elements(execution_url, params={'all_elements': 'ON', 'comment_filter': 'OFF'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 7)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_1)
        self.assertEqual(elements[2]['elem_id'], step_id_1_2)   
        self.assertEqual(elements[3]['elem_id'], paragraph_id_2) 
        self.assertEqual(elements[4]['elem_id'], section_id_3)
        self.assertEqual(elements[5]['elem_id'], step_id_3_1)
        self.assertEqual(elements[6]['elem_id'], step_id_3_2)   
        
        elements = self.get_elements(execution_url, params={'all_elements': 'ON', 'comment_filter': 'ON'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 7)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_1)
        self.assertEqual(elements[2]['elem_id'], step_id_1_2)   
        self.assertEqual(elements[3]['elem_id'], paragraph_id_2) 
        self.assertEqual(elements[4]['elem_id'], section_id_3)
        self.assertEqual(elements[5]['elem_id'], step_id_3_1)
        self.assertEqual(elements[6]['elem_id'], step_id_3_2)             
        
        elements = self.get_elements(execution_url, params={'all_elements': 'ON', 'comment_filter': 'ON', 'limit': 2})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_1)
        
        elements = self.get_elements(execution_url, params={'all_elements': 'ON', 'comment_filter': 'ON', 'offset': 1, 'limit': 2})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], step_id_1_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_2)          
        
        # add AR comment  
        res_dict = self.add_conversation(execution_url, step_id_1_1, {'type': 'ACTIVITY_REPORT_COMMENT'})
        res_dict = self.add_conversation(execution_url, step_id_1_2, {'type': 'ACTIVITY_REPORT_COMMENT'})
        
        # add DR comment  
        res_dict = self.add_conversation(execution_url, section_id_1, {'type': 'DATA_REVIEW_COMMENT'})
        res_dict = self.add_conversation(execution_url, paragraph_id_2, {'type': 'DATA_REVIEW_COMMENT'})   
        
        elements = self.get_elements(execution_url, params={'comment_filter': 'ON'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0]['elem_id'], step_id_1_1)
        self.assertEqual(elements[1]['elem_id'], section_id_3)
        self.assertEqual(elements[2]['elem_id'], step_id_3_1)         
        
        elements = self.get_elements(execution_url, params={'ar_comment_filter': 'ON'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], step_id_1_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_2)
        
        elements = self.get_elements(execution_url, params={'dr_comment_filter': 'ON'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], paragraph_id_2)
        
        elements = self.get_elements(execution_url, params={'comment_filter': 'ON', 'ar_comment_filter': 'ON'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 4)
        self.assertEqual(elements[0]['elem_id'], step_id_1_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_2)
        self.assertEqual(elements[2]['elem_id'], section_id_3)
        self.assertEqual(elements[3]['elem_id'], step_id_3_1)
        
        elements = self.get_elements(execution_url, params={'comment_filter': 'ON', 
            'ar_comment_filter': 'ON', 
            'dr_comment_filter': 'ON'})
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 6)
        self.assertEqual(elements[0]['elem_id'], section_id_1)
        self.assertEqual(elements[1]['elem_id'], step_id_1_1)
        self.assertEqual(elements[2]['elem_id'], step_id_1_2)
        self.assertEqual(elements[3]['elem_id'], paragraph_id_2)         
        self.assertEqual(elements[4]['elem_id'], section_id_3)
        self.assertEqual(elements[5]['elem_id'], step_id_3_1)  
        
        elements = self.get_elements(execution_url, params={'comment_filter': 'ON', 
            'ar_comment_filter': 'ON', 
            'dr_comment_filter': 'ON',
            'offset': 2,
            'limit': 3})        
        # logger.debug('elements: %s', json.dumps(elements, indent=4))
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0]['elem_id'], step_id_1_2)
        self.assertEqual(elements[1]['elem_id'], paragraph_id_2)         
        self.assertEqual(elements[2]['elem_id'], section_id_3)           

    def test_files(self):
        id_dict = self.create_execution_example()

        execution_url = id_dict['execution_url']
        execution_id = id_dict['execution_id']
        section_id_1 = id_dict['section_id_1']
        step_id_1_1 = id_dict['step_id_1_1']

        # Add comment to section
        res_dict = self.add_conversation(execution_url, section_id_1, {'type': 'COMMENT'})
        conversation_id = res_dict['conversation_id']
        comment_1 = res_dict['comments'][0]
        comment_id_1 = comment_1['comment_id']
        
        content1 = 'This is the first comment for the section'
        res_dict = self.update_comment(execution_url, section_id_1, conversation_id, comment_id_1, content1)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['content'], content1)        

        # Add File to comment
        fileUrl1 = "location/path/to/file"
        res_dict = self.add_comment_file_meta(execution_url, section_id_1, conversation_id, comment_id_1, fileUrl1)
        comment_file_id_1 = res_dict['file_id']

        fileUrl2 = "location/path/to/file2"
        res_dict = self.add_comment_file_meta(execution_url, section_id_1, conversation_id, comment_id_1, fileUrl2)
        comment_file_id_2 = res_dict['file_id']

        #Get File from comment
        res_dict = self.get_comment_file(execution_url, section_id_1, conversation_id, comment_id_1, comment_file_id_1)
        self.assertEqual(res_dict['url'], fileUrl1)

        #Get files from comments
        res_dict = self.get_comment_files(execution_url, section_id_1, conversation_id, comment_id_1)
        logger.debug('res_dict: %s', json.dumps(res_dict, indent=4))
        
        self.assertEqual(len(res_dict), 2)
        self.assertEqual(res_dict[0]['url'], fileUrl1)
        self.assertEqual(res_dict[1]['url'], fileUrl2)

        res_dict = self.get_comment_files(execution_url, section_id_1, conversation_id, comment_id_1, offset=1, limit=1)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)

        #delete commment file
        self.delete_comment_file(execution_url, section_id_1, conversation_id, comment_id_1, comment_file_id_1)
        
        res_dict = self.get_comment_files(execution_url, section_id_1, conversation_id, comment_id_1)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)

        # Add File to execution
        res_dict = self.add_exec_file_meta(execution_id, fileUrl1)
        exec_file_id_1 = res_dict['file_id']

        res_dict = self.add_exec_file_meta(execution_id, fileUrl2)
        exec_file_id_2 = res_dict['file_id']

        #Get File from comment
        res_dict = self.get_exec_file(execution_id, exec_file_id_1)
        self.assertEqual(res_dict['url'], fileUrl1)

        #Get files from comments
        url = '{0}/executions/{1}/files'.format(shared_dict['host'], execution_id)
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
        self.delete_exec_file(execution_id, exec_file_id_1)
        logger.debug('GET: %s', url)
        result = requests.get(url,
            headers=shared_dict['headers'])
        res_dict = json.loads(result.text)
        self.assertEqual(int(result.headers['x-total-count']), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)

        # Add File to element
        fileUrl1 = "location/path/to/file"
        res_dict = self.add_elem_file_meta(execution_url, section_id_1, fileUrl1)
        elem_file_id_1 = res_dict['file_id']

        fileUrl2 = "location/path/to/file2"
        res_dict = self.add_elem_file_meta(execution_url, section_id_1, fileUrl2)
        elem_file_id_2 = res_dict['file_id']

        #Get File from element
        res_dict = self.get_elem_file(execution_url, section_id_1, elem_file_id_1)
        self.assertEqual(res_dict['url'], fileUrl1)

        #Get files from elements
        url = '{0}/executions/{1}/elements/{2}/files'.format(shared_dict['host'], execution_id, section_id_1)
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
        self.delete_elem_file(execution_url, section_id_1, elem_file_id_1)
        logger.debug('GET: %s', url)
        result = requests.get(url,
            headers=shared_dict['headers'])
        res_dict = json.loads(result.text)
        self.assertEqual(len(res_dict), 1)
        self.assertEqual(res_dict[0]['url'], fileUrl2)



    def create_execution_example(self):
        id_dict = {}

        ## Add a venue
        venue_id, venue_name = self.create_venue2()

        ## Add an execution
        description = 'My new execution'
        res_dict = self.create_execution(venue_id, description)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))

        ## Check execution
        execution_id = res_dict['execution_id']
        id_dict['execution_id'] = execution_id
        execution_url = shared_dict['host'] + '/executions/' + execution_id

        id_dict['execution_url'] = execution_url

        time_started_str = res_dict['time_started']
        time_started = parser.parse(time_started_str)
        time_now_utc = datetime.now(dateutil.tz.tzutc())
        logger.debug('time_started_str: %s', time_started_str)
        logger.debug('time_started: %s', time_started)
        logger.debug('time_now_utc: %s', time_now_utc)
        time_delta = time_started - time_now_utc if time_started > time_now_utc else time_now_utc - time_started
        logger.debug('time_delta.days: %s', time_delta.days)
        logger.debug('time_delta.seconds: %s', time_delta.seconds)

        self.assertEqual(res_dict['venue_id'], venue_id)
        self.assertEqual(res_dict['description'], description)

        self.assertLess(math.fabs(time_delta.seconds)+24*3600*math.fabs(time_delta.days), 50910.0)
        self.assertEqual(res_dict['venue_name'], venue_name)
        # self.assertEqual(res_dict['url'], execution_url)

        result = requests.get(execution_url, headers=shared_dict['headers'])
        self.assertEqual(result.status_code, 200)
        res_dict = json.loads(result.text)
        self.assertEqual(res_dict['venue_id'], venue_id)
        self.assertEqual(res_dict['description'], description)

        ## Add section 1
        res_dict = self.add_section(base_url=execution_url,
            insert_after_id='-1',
            level='',
            title='Section 1',
            description='Section 1')

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))

        section_id_1 = res_dict['elem']['elem_id']
        self.assertEqual(res_dict['elem']['parent_id'], '')
        id_dict['section_id_1'] = section_id_1
        self.assertEqual(res_dict['elem']['number'], '1')
        self.assertEqual(len(res_dict['numbers']), 1)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_id_1)  
        self.assertEqual(res_dict['numbers'][0]['number'], '1')       
        self.assertEqual(len(res_dict['elem_ids']), 1)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)

        ## Add step 1-1
        notices = [
            {
                'category': 'TESTBED_WARNING',
                'message': 'This is a warning for test bed'
            },
            {
                "category": "PERSONNEL_CAUTION",
                "message": "This is a caution for personnel"
            }
        ]

        res_dict = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=section_id_1,
            level='CHILD',
            title='Step 1-1',
            guard='',
            variable_name='manual_input_1_1_var',
            code_name='manual_input_step.run',
            code_commit='commit-hash-3dfaea',
            code_release='1.0',
            notices=notices)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        step_id_1_1 = res_dict['elem']['elem_id']
        id_dict['step_id_1_1'] = step_id_1_1
        self.assertEqual(res_dict['elem']['parent_id'], section_id_1)
        self.assertEqual(res_dict['elem']['number'], '1-1')
        self.assertEqual(len(res_dict['numbers']), 1)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_id_1_1)  
        self.assertEqual(res_dict['numbers'][0]['number'], '1-1')           
        self.assertEqual(len(res_dict['elem_ids']), 2)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)
        self.assertEqual(res_dict['elem_ids'][1], step_id_1_1)

        ## Add step 1-2
        res_dict = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=step_id_1_1,
            level='SIBLING',
            title='Step 1-2',
            guard='',
            variable_name='manual_input_1_2_var',
            code_name='manual_input_step.run',
            code_commit='commit-hash-3dfaea',
            code_release='1.0',
            notices=[])

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        step_id_1_2 = res_dict['elem']['elem_id']
        id_dict['step_id_1_2'] = step_id_1_2
        self.assertEqual(res_dict['elem']['parent_id'], section_id_1)
        self.assertEqual(res_dict['elem']['number'], '1-2')
        self.assertEqual(len(res_dict['numbers']), 1)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_id_1_2)  
        self.assertEqual(res_dict['numbers'][0]['number'], '1-2')           
        self.assertEqual(len(res_dict['elem_ids']), 3)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)
        self.assertEqual(res_dict['elem_ids'][1], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][2], step_id_1_2)

        ## Add section 3
        res_dict = self.add_section(base_url=execution_url,
            insert_after_id=section_id_1,
            level='SIBLING',
            title='Section 3')

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        section_id_3 = res_dict['elem']['elem_id']
        id_dict['section_id_3'] = section_id_3
        self.assertEqual(res_dict['elem']['parent_id'], '')
        self.assertEqual(res_dict['elem']['number'], '2')
        self.assertEqual(len(res_dict['numbers']), 1)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], section_id_3)  
        self.assertEqual(res_dict['numbers'][0]['number'], '2')           
        self.assertEqual(len(res_dict['elem_ids']), 4)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)
        self.assertEqual(res_dict['elem_ids'][1], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][2], step_id_1_2)
        self.assertEqual(res_dict['elem_ids'][3], section_id_3)

        ## Add step 3-1
        res_dict = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=section_id_3,
            level='CHILD',
            title='Step 3-1',
            guard='',
            variable_name='manual_input_3_1_var',
            code_name='manual_input_step.run',
            code_commit='commit-hash-3dfaea',
            code_release='1.0',
            notices=[])
        step_id_3_1 = res_dict['elem']['elem_id']
        id_dict['step_id_3_1'] = step_id_3_1

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['elem']['parent_id'], section_id_3)
        self.assertEqual(res_dict['elem']['number'], '2-1')
        self.assertEqual(len(res_dict['numbers']), 1)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_id_3_1)  
        self.assertEqual(res_dict['numbers'][0]['number'], '2-1')           
        self.assertEqual(len(res_dict['elem_ids']), 5)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)
        self.assertEqual(res_dict['elem_ids'][1], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][2], step_id_1_2)
        self.assertEqual(res_dict['elem_ids'][3], section_id_3)
        self.assertEqual(res_dict['elem_ids'][4], step_id_3_1)

        ## Add step 3-2
        res_dict = self.add_step_generic(base_url=execution_url,
            step_type=StepTypes.MANUAL_INPUT,
            insert_after_id=step_id_3_1,
            level='SIBLING',
            title='Step 3-2',
            guard='',
            variable_name='manual_input_3_2_var',
            code_name='manual_input_step.run',
            code_commit='commit-hash-3dfaea',
            code_release='1.0',
            notices=[])

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        step_id_3_2 = res_dict['elem']['elem_id']
        id_dict['step_id_3_2'] = step_id_3_2
        self.assertEqual(res_dict['elem']['parent_id'], section_id_3)
        self.assertEqual(res_dict['elem']['number'], '2-2')
        self.assertEqual(len(res_dict['numbers']), 1)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], step_id_3_2)  
        self.assertEqual(res_dict['numbers'][0]['number'], '2-2')           
        self.assertEqual(len(res_dict['elem_ids']), 6)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)
        self.assertEqual(res_dict['elem_ids'][1], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][2], step_id_1_2)
        self.assertEqual(res_dict['elem_ids'][3], section_id_3)
        self.assertEqual(res_dict['elem_ids'][4], step_id_3_1)
        self.assertEqual(res_dict['elem_ids'][5], step_id_3_2)

        ## add paragraph
        res_dict = self.add_paragraph(base_url=execution_url,
            insert_after_id=section_id_1,
            level='SIBLING',
            title='Paragraph Section 1')
        logger.debug('paragraph res_dict= %s', json.dumps(res_dict, indent=4))

        as_run_dict = self.get_as_run(execution_id)
        logger.debug('as_run_dict= %s', json.dumps(as_run_dict, indent=4))  

        paragraph_id_2 = res_dict['elem']['elem_id']
        id_dict['paragraph_id_2'] = paragraph_id_2
        self.assertEqual(res_dict['elem']['parent_id'], '')
        self.assertEqual(res_dict['elem']['number'], '2')
        self.assertEqual(len(res_dict['numbers']), 4)
        self.assertEqual(res_dict['numbers'][0]['elem_id'], paragraph_id_2)  
        self.assertEqual(res_dict['numbers'][0]['number'], '2')           
        self.assertEqual(len(res_dict['elem_ids']), 7)
        self.assertEqual(res_dict['elem_ids'][0], section_id_1)
        self.assertEqual(res_dict['elem_ids'][1], step_id_1_1)
        self.assertEqual(res_dict['elem_ids'][2], step_id_1_2)
        self.assertEqual(res_dict['elem_ids'][3], paragraph_id_2)
        self.assertEqual(res_dict['elem_ids'][4], section_id_3)
        self.assertEqual(res_dict['elem_ids'][5], step_id_3_1)
        self.assertEqual(res_dict['elem_ids'][6], step_id_3_2)

        return id_dict

    #### Execution status TESTS

    def test_set_execution_status(self):
        logger.debug('test_set_execution_status')
        ## Add a venue
        venue_id, venue_name = self.create_venue2()
        ## Add an execution
        description = 'My new execution to set its status'
        res_dict = self.create_execution(venue_id, description)
        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))

        execution_id = res_dict['execution_id']

        ## get status
        url = shared_dict['host'] + '/executions/' + execution_id + '/status'
        logger.debug('url= %s', url)
        result = requests.get(url,
            headers=shared_dict['headers'])
        res_dict = json.loads(result.text)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(res_dict['status'], 'IDLE')

        ## set status
        status_dict = {'status': 'CLOSED'}
        result = requests.post(url,
            headers=shared_dict['headers'],
            data=json.dumps(status_dict))

        logger.debug('result.status_code= %s', result.status_code)
        self.assertEqual(result.status_code, 200)

        ## get status again
        result = requests.get(url,
            headers=shared_dict['headers'])
        res_dict = json.loads(result.text)

        logger.debug('res_dict= %s', json.dumps(res_dict, indent=4))
        self.assertEqual(res_dict['status'], 'CLOSED')
        self.assertEqual(result.status_code, 200)


    def update_comment(self, execution_url, elem_id, conversation_id, comment_id, content, code_expected=200):
        comment_dict = {'content': content}

        url = '{0}/elements/{1}/conversations/{2}/comments/{3}'.format(execution_url, elem_id, 
            conversation_id, comment_id)

        logger.debug('PATCH: %s', url)
        result = requests.patch(url,
            headers=shared_dict['headers'],
            data=json.dumps(comment_dict))

        self.assertEqual(result.status_code, code_expected)

        res_dict = json.loads(result.text)

        return res_dict   

    def get_next_element(self, execution_url, elem_id, executable, code_expected=200):
        url = '{0}/next_elem'.format(execution_url)
        params = {'elem_id': elem_id, 'executable': 'true' if executable else 'false'}
        logger.debug('GET: %s', url)
        result = requests.get(url,
            params = params,
            headers=shared_dict['headers'])

        self.assertEqual(result.status_code, code_expected)

        res_dict = json.loads(result.text)

        return res_dict       

    def set_boundary_element(self, execution_url, elem_id, code_expected=200):
        url = '{0}/boundary_elem'.format(execution_url)
        params = {'elem_id': elem_id}
        logger.debug('POST: %s', url)
        result = requests.post(url,
            params = params,
            headers=shared_dict['headers'])

        self.assertEqual(result.status_code, code_expected)

        res_dict = json.loads(result.text)

        return res_dict  


    def update_elements(self, base_url, elems_input, code_expected=200):
        url = '{0}/elements'.format(base_url)
        params = {'elems_input': elems_input}
        logger.debug('PATCH: %s', url)
        result = requests.patch(url,
            params = params,
            headers=shared_dict['headers'],
            json=elems_input)

        self.assertEqual(result.status_code, code_expected)

        res_dict = json.loads(result.text)

        return res_dict          

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./test-reports/"))
