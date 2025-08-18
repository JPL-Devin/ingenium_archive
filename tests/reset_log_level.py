import requests
import json
import time
import os

res = requests.post('http://localhost:8529/_db/_system/_open/auth', 
    json={'username': 'root', 'password': os.getenv('ARANGO_ROOT_PASSWORD')})
print('login:', res.status_code)
res_dict = res.json()

token = res_dict['jwt']
headers = {'Authorization': f'bearer {token}'}

res = requests.get('http://localhost:8529/_db/ingenium/_admin/log/level', headers=headers)
print('log levels:', res.status_code)
orig_levels = res.json()
print(json.dumps(orig_levels, indent=4))

default_levels = {
    "agency": "INFO",
    "agencycomm": "INFO",
    "authentication": "DEFAULT",
    "authorization": "DEFAULT",
    "cache": "INFO",
    "cluster": "INFO",
    "collector": "DEFAULT",
    "communication": "INFO",
    "compactor": "DEFAULT",
    "config": "DEFAULT",
    "datafiles": "INFO",
    "development": "FATAL",
    "engines": "INFO",
    "general": "INFO",
    "graphs": "INFO",
    "heartbeat": "INFO",
    "httpclient": "WARNING",
    "memory": "WARNING",
    "mmap": "DEFAULT",
    "performance": "WARNING",
    "pregel": "INFO",
    "queries": "INFO",
    "replication": "INFO",
    "requests": "FATAL",
    "rocksdb": "WARNING",
    "ssl": "WARNING",
    "startup": "INFO",
    "supervision": "INFO",
    "syscall": "INFO",
    "threads": "WARNING",
    "trx": "WARNING",
    "v8": "WARNING",
    "views": "FATAL"
}
res = requests.put('http://localhost:8529/_db/ingenium/_admin/log/level', json=default_levels, headers=headers)
print('reverted log levels:', res.status_code)
res_dict = res.json()
print(json.dumps(res_dict, indent=4))