import requests
import json

url = 'http://localhost:8010/executions'
headers = {'Content-Type': 'application/json',
           'Accept': 'application/json'}
execution_dict = {"description": "swag", "venue_id": "lmao"}

print(json.dumps(execution_dict))

result = requests.post(url,
    headers=headers,
    data=json.dumps(execution_dict))
print(result.status_code)

if result.status_code == 200:
    res_dict = json.loads(result.text)
    print(json.dumps(res_dict, indent=4))
    url = 'http://localhost:8010/executions/' + res_dict['execution_id']
    result = requests.get(url)
    print(result.status_code)
    res_dict = json.loads(result.text)
    print(json.dumps(res_dict, indent=4))

    execution_update_dict = {
      'description': "never made it was a wise man, couldnt cut it as a poor man stealing" #,
      # 'name': res_dict['name']
    }
    result = requests.put(url,
        headers=headers,
        data=json.dumps(execution_update_dict))
    print(result.status_code)
    result = requests.get(url)
    print(result.status_code)

    res_dict = json.loads(result.text)
    print(json.dumps(res_dict, indent=4))
    execution_id = res_dict['execution_id']
    url = 'http://localhost:8010/executions/' + execution_id + '/status'
    status_dict = {'status': 'RUNNING'}
    result = requests.put(url,
        headers=headers,
        data=json.dumps(status_dict))
    print(result.status_code)


    url = 'http://localhost:8010/executions/' + execution_id + '/steps?level=CHILD'
    step_dict = { "elem_id": "string", "elem_type": "STEP", "execution_id": "string", "description": "STEP ONE", "number": "string", "step_type": "MANUAL_INPUT", "variable": {   "name": "string" }, "code": {   "name": "string",   "commit": "Latest",   "release": "Latest" }, "guard": "string", "notices": [   {     "category": "TESTBED_WARNING",     "message": "string"   } ]}
    print("STATUS GOT")
    result = requests.post(url,
        headers=headers,
        data=json.dumps(step_dict))
    res_dict1 = json.loads(result.text)
    print("STEP ONE")
    print(json.dumps(res_dict1, indent=4))

    url = 'http://localhost:8010/executions/' + execution_id + '/steps?insert_after_id=' + res_dict1['elem_id'] + '&level=SIBLING'
    step_dict = { "elem_id": "string", "elem_type": "STEP", "execution_id": "string", "description": "STEP TWO", "number": "string", "step_type": "MANUAL_INPUT", "variable": {   "name": "string" }, "code": {   "name": "string",   "commit": "Latest",   "release": "Latest" }, "guard": "string", "notices": [   {     "category": "TESTBED_WARNING",     "message": "string"   } ]}
    result = requests.post(url,
        headers=headers,
        data=json.dumps(step_dict))

    res_dict = json.loads(result.text)
    print("STEP TWO")
    print(json.dumps(res_dict, indent=4))
    url = 'http://localhost:8010/executions/' + execution_id + '/sections?insert_after_id=' + res_dict1['elem_id'] + '&level=SIBLING'
    section_dict = { "elem_type": "SECTION", "description": "SECTION ONE AFTER STEP ONE BEFORE STEP TWO", "number": "string"}
    result = requests.post(url,
        headers=headers,
        data=json.dumps(section_dict))

    res_dict = json.loads(result.text)
    print("SECTION One")
    print(json.dumps(res_dict, indent=4))

    url = 'http://localhost:8010/executions/' + execution_id + '/steps?insert_after_id=' + res_dict['elem_id'] + '&level=CHILD'
    step_dict = { "elem_id": "string", "elem_type": "STEP", "execution_id": "string", "description": "STEP WITHIN SECTION ONE", "number": "string", "step_type": "MANUAL_INPUT", "variable": {   "name": "string" }, "code": {   "name": "string",   "commit": "Latest",   "release": "Latest" }, "guard": "string", "notices": [   {     "category": "TESTBED_WARNING",     "message": "string"   } ]}
    result = requests.post(url,
        headers=headers,
        data=json.dumps(step_dict))

    res_dict = json.loads(result.text)
    print("STEP Four")
    print(json.dumps(res_dict, indent=4))

    url = 'http://localhost:8010/steps/' + res_dict1['elem_id'] + '/result'
    step_dict = {"Rockstar":"And we All Wanna be big rockstars living in top houses driving 15 cars"}
    result = requests.put(url,
        headers=headers,
        data=json.dumps(step_dict))

    print("Result For Step One")

    url = 'http://localhost:8010/steps/' + res_dict1['elem_id']
    step_dict = {"description": "BUT THE TIGERS CAME AT NIGHT, THEIR VOICES SOFT AS THUNDER"}
    result = requests.put(url,
        headers=headers,
        data=json.dumps(step_dict))

    res_dict = json.loads(result.text)
    print("Upadte & Version Step One")
    print(json.dumps(res_dict, indent=4))