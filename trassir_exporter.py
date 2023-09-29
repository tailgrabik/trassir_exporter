import requests
import yaml
import prometheus_client
import urllib3
import json
urllib3.disable_warnings()


def login():
    payload={'username': 'prometheus', 'password':'CgkxGQaz5aOyR832'}
    req=requests.get("https://192.168.2.80:8080/login",params=payload,verify=False)
    res = json.loads(req.text)
    if res['success'] == 1:
        return res['sid']
    else:
        return False
def get_data(comm,auth):
    payload={'sid': auth}
    req=requests.post(f'https://192.168.2.80:8080/{comm}',params=payload,verify=False)
    print(req.text)
get_data('health',login())