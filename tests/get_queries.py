import requests
import json
import os

res = requests.post('http://localhost:8529/_db/_system/_open/auth', 
    json={'username': 'root', 'password': os.getenv('ARANGO_ROOT_PASSWORD')})
print('login:', res.status_code)
res_dict = res.json()

token = res_dict['jwt']

headers = {'Authorization': f'bearer {token}'}

res = requests.get('http://localhost:8529/_db/ingenium/_api/query/current', headers=headers)
print('current queries:', res.status_code)
res_dict = res.json()
print(json.dumps(res_dict, indent=4))

res = requests.get('http://localhost:8529/_db/ingenium/_api/query/slow', headers=headers)
print('slow queries:', res.status_code)
res_dict = res.json()

print(json.dumps(res_dict, indent=4))

res = requests.get('http://localhost:8529/_db/ingenium/_admin/statistics', headers=headers)
print('statistics:', res.status_code)
res_dict = res.json()
print(json.dumps(res_dict, indent=4))

res = requests.get('http://localhost:8529/_db/ingenium/_admin/wal/properties', headers=headers)
print('wal properties:', res.status_code)
res_dict = res.json()
print(json.dumps(res_dict, indent=4))