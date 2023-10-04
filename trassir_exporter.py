import httpx
import yaml
from prometheus_client import Gauge,Counter
from prometheus_client import start_http_server
import json
import argparse
import sys
import time
import logging

root = logging.getLogger()
root.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='trassir_exporter.yml')
    parser.add_argument('--metric_port', default='10001')
    parser.add_argument('--scrape_interval', default='10')
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
    try:
        payload = {'username': config['trassir_user'], 'password':config['trassir_password']}
        req = httpx.post(f"https://{config['trassir_addr']}:{config['trassir_port']}/login",params=payload,verify=False)
        res = json.loads(req.text)
        if res['success'] == 1:
            logging.info(res['success'])
            return res['sid']
        else:
            logging.error(res['sid'])
            return False
            
    except Exception as e:
        logging.error(e)
        exit()

def get_data(comm,auth):
    try:
        payload = {'sid': auth}
        req = httpx.post(f"https://{config['trassir_addr']}:{config['trassir_port']}/{comm}",params=payload,verify=False)
        return json.loads(req.text)
    except Exception as e:
        logging.error(e)
        exit()

def load_config(namespace):
    config={}
    params=['metric_port','scrape_interval','trassir_port','trassir_addr','trassir_user','trassir_password']
    try:    
        with open(namespace.config,'r') as f:
            config = yaml.safe_load(f)
            for param in params:
                check_config_value(config,param,getattr(namespace,param)) 
    except Exception as e:
        logging.error(e)
        
        for param in params:
            config[param] = getattr(namespace, param)
    return config


trassir_disk_health = Gauge('trassir_disk_health','Disk health trassir server')
trassir_database_health = Gauge('trassir_database_health','Database health trassir')
trassir_channels_total = Gauge('trassir_channels_total','Total channels trassir server')
trassir_channels_online = Gauge('trassir_channels_online','Online channels trassir server')
trassir_uptime = Gauge('trassir_uptime','Trassir uptime')
trassir_cpu_load = Gauge('trassir_cpu_load','Trassir CPU usage')
trassir_network_status = Gauge('trassir_network_status','Trassir network status')
trassir_automation_status = Gauge('trassir_automation_status','Trassir automation status')
trassir_archive_main_days = Gauge('trassir_archive_main_days','Archive main days')
trassir_archive_subs_days = Gauge('trassir_archive_subs_days','Archive subs days')
trassir_archive_priv_days = Gauge('trassir_archive_priv_days','Archive priv days')


def update_metrics(data):
    try:
        trassir_disk_health.set(data['disks'])
        trassir_database_health.set(data['database'])
        trassir_channels_total.set(data['channels_total'])
        trassir_channels_online.set(data['channels_online'])
        trassir_uptime.set(data['uptime'])
        trassir_cpu_load.set(data['cpu_load'])
        trassir_network_status.set(data['network'])
        trassir_automation_status.set(data['automation'])
        trassir_archive_main_days.set(data['disks_stat_main_days'])
        trassir_archive_subs_days.set(data['disks_stat_subs_days'])
        trassir_archive_priv_days.set(data['disks_stat_priv_days'])
    except Exception as e:
        logging.error(e)
        exit()

parser = create_parser()
namespace = parser.parse_args(sys.argv[1:])
config = load_config(namespace)
sid = login()
try:
    start_http_server(int(config['metric_port']))
except Exception as e:
    logging.error(e)
    exit()
while True:
    data = get_data('health',sid)
    update_metrics(data)
    time.sleep(int(config['scrape_interval']))