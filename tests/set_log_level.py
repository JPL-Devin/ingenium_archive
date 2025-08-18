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

log_levels = {
    "agency": "DEBUG",
    "agencycomm": "DEBUG",
    "authentication": "DEBUG",
    "authorization": "DEBUG",
    "cache": "DEBUG",
    "cluster": "DEBUG",
    "collector": "DEBUG",
    "communication": "DEBUG",
    "compactor": "DEBUG",
    "config": "DEBUG",
    "datafiles": "DEBUG",
    "development": "DEBUG",
    "engines": "DEBUG",
    "general": "DEBUG",
    "graphs": "DEBUG",
    "heartbeat": "DEBUG",
    "httpclient": "DEBUG",
    "memory": "DEBUG",
    "mmap": "DEBUG",
    "performance": "DEBUG",
    "pregel": "DEBUG",
    "queries": "INFO",
    "replication": "DEBUG",
    "requests": "WARNING",
    "rocksdb": "DEBUG",
    "ssl": "DEBUG",
    "startup": "DEBUG",
    "supervision": "DEBUG",
    "syscall": "DEBUG",
    "threads": "DEBUG",
    "trx": "DEBUG",
    "v8": "DEBUG",
    "views": "DEBUG"
}

res = requests.put('http://localhost:8529/_db/ingenium/_admin/log/level', json=log_levels, headers=headers)
print('updated log levels:', res.status_code)
res_dict = res.json()
print(json.dumps(res_dict, indent=4))
