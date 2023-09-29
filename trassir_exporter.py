import httpx
import yaml
import prometheus_client
import json
import argparse
import sys

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='trassir_exporter.yml')
    parser.add_argument('--metric_port', default='10001')
    parser.add_argument('--trassir_port', default='8080')
    parser.add_argument('--trassir_addr', default='192.168.1.1')
    parser.add_argument('--trassir_user', default='prometheus')
    parser.add_argument('--trassir_password', default='password')
    return parser

def check_config_value(config,key,val):
    if key not in config.keys():
        config[key] = val
    if not config[key]:
        config[key]=val


def login():
    payload = {'username': 'prometheus', 'password':'CgkxGQaz5aOyR832'}
    req = httpx.get("https://192.168.2.80:8080/login",params=payload,verify=False)
    res = json.loads(req.text)
    if res['success'] == 1:
        return res['sid']
    else:
        return False
def get_data(comm,auth):
    payload = {'sid': auth}
    req = httpx.post(f'https://192.168.2.80:8080/{comm}',params=payload,verify=False)
    return req.text

def load_config(namespace):
    config={}
    params=['metric_port','trassir_port','trassir_addr','trassir_user','trassir_password']
    try:    
        with open(namespace.config,'r') as f:
            config = yaml.safe_load(f)
            for param in params:
                check_config_value(config,param,getattr(namespace,param)) 
    except:
        for param in params:
            config[param] = getattr(namespace, param)
    return config

parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])
config = load_config(namespace)
