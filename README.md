# Prometheus trassir exporter

Trassir prometheus exporter health metrics Trassir CCTV server: https://trassir.ru/
Uses the health API method

## Example metric

```
trassir_disk_health 1.0
# HELP trassir_database_health Database health trassir
# TYPE trassir_database_health gauge
trassir_database_health 1.0
# HELP trassir_channels_total Total channels trassir server
# TYPE trassir_channels_total gauge
trassir_channels_total 104.0
# HELP trassir_channels_online Online channels trassir server
# TYPE trassir_channels_online gauge
trassir_channels_online 104.0
# HELP trassir_uptime Trassir uptime
# TYPE trassir_uptime gauge
trassir_uptime 536009.0
# HELP trassir_cpu_load Trassir CPU usage
# TYPE trassir_cpu_load gauge
trassir_cpu_load 70.82
# HELP trassir_network_status Trassir network status
# TYPE trassir_network_status gauge
trassir_network_status 1.0
# HELP trassir_automation_status Trassir automation status
# TYPE trassir_automation_status gauge
trassir_automation_status 1.0
# HELP trassir_archive_main_days Archive main days
# TYPE trassir_archive_main_days gauge
trassir_archive_main_days 14.51
# HELP trassir_archive_subs_days Archive subs days
# TYPE trassir_archive_subs_days gauge
trassir_archive_subs_days 59.56
# HELP trassir_archive_priv_days Archive priv days
# TYPE trassir_archive_priv_days gauge
trassir_archive_priv_days 0.0
```
## Installation

### Venv Run

1. git clone
2. python3 -m venv /path/to/clone
3. cd /path/to/clone
4. source /path/to/clone/bin/activate
5. pip install -f freeze
6. create config 
7. start exporter
(option)
8. create systemd service touch /etc/systemd/system/trassir_exporter.service
```
[Unit]
Description=Prometheus Trassir Exporter
After=network-online.target

[Service]
Type=simple
User=root
Group=root
ExecStart=/opt/trassir_exporter/bin/python /opt/trassir_exporter/trassir_exporter.py --config /etc/exporters/trassir.yml
SyslogIdentifier=mikrotik_exporter
Restart=always
RestartSec=1
StartLimitInterval=0

[Install]
WantedBy=multi-user.target

```
9. systemctl daemon-reload
10. systemctl --now enable trassir_exporter.service
11. All done!

### Docker

1. create config 
2. docker run --restart=always -d -v <source_config>:/usr/src/app/trassir.yml -p<port>:<port> -it --name trassir_exporter trassir_exporter:latest

## Example config
trassir.yml
```
metric_port: 10001
scrape_interval: 10
trassir_port: 8080
trassir_addr: '192.168.1.2'
trassir_user: prometheus
trassir_password: password

```
