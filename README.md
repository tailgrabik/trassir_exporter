# trassir_exporter

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