import requests
import yaml
import prometheus_client
# import urllib3

# urllib3.disable_warnings()

def login():
    payload={'username': 'prometheus', 'password':'1111'}
    req=requests.get("https://192.168.1.80:8080/login",params=payload,verify=False)
    print(req.text)
login()
#get_data('health')