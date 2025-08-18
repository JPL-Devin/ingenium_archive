import requests
import json
import random

# host = 'http://localhost:8010'
host = 'http://100.64.153.225:8010'
if True:
    url = host + '/venues'
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    idx_str = str(random.randint(0,10000))
    venue_dict = {'name': 'wsts-' + idx_str, 'description': 'WSTS machine in Bld ' + idx_str}
    result = requests.post(url,
        headers=headers,
        data=json.dumps(venue_dict))
    print(result.status_code)

    if result.status_code == 200:
        res_dict = json.loads(result.text)
        print(json.dumps(res_dict, indent=4))

        url = host + '/venues/' + res_dict['venue_id']

        result = requests.get(url)
        print(result.status_code)
        if result.status_code == 200:
            res_dict = json.loads(result.text)
            print(json.dumps(res_dict, indent=4))

        venue_update_dict = {
          'location': 'room' + str(random.randint(101,299)) #,
          # 'name': res_dict['name']
        }
        result = requests.put(url,
            headers=headers,
            data=json.dumps(venue_update_dict))
        print(result.status_code)

        result = requests.get(url)
        print(result.status_code)
        if result.status_code == 200:
            res_dict = json.loads(result.text)
            print(json.dumps(res_dict, indent=4))
        venue_id = res_dict['venue_id']
        url = host + '/venues/' + venue_id + '/status'
        venue_status_dict = {'status': 'AVAILABLE'};
        result = requests.put(url,
            headers=headers,
            data=json.dumps(venue_status_dict))
        print(result.status_code)
        print(result.text)

        result = requests.get(url)
        print(result.status_code)
        # TODO: server needs to return error in JSON format
        if result.status_code == 200:
            res_dict = json.loads(result.text)
            print(json.dumps(res_dict, indent=4))

        url = host + '/venues/' + venue_id
        result = requests.get(url)
        print(result.status_code)
        if result.status_code == 200:
            res_dict = json.loads(result.text)
            print(json.dumps(res_dict, indent=4))

if False:
    url = host + '/venues'
    result = requests.get(url)
    print('DELETE code=', result.status_code)

if False:
    url = host + '/venues'
    result = requests.get(url)
    print(result.status_code)
    if result.status_code == 200:
        res_dict = json.loads(result.text)
        for venue in res_dict:
            venue_id = venue['venue_id']
            url = host + '/venues/' + venue_id

            result = requests.get(url)
            print(result.status_code)
            if result.status_code == 200:
                res_dict = json.loads(result.text)
                print(json.dumps(res_dict, indent=4))

            result = requests.delete(url)
            print('DELETE code=', result.status_code)

if False:
    url = host + '/venues'
    result = requests.get(url)
    print(result.status_code)
    if result.status_code == 200:
        res_dict = json.loads(result.text)
        print(json.dumps(res_dict, indent=4))
    else:
        print(result.text)
