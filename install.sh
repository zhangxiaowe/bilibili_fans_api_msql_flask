#!/bin/bash

sudo tee /etc/systemd/system/my_bilibili_api_service1.service >/dev/null << EOF
[Unit]
Description=My Python Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/bilibili_fans_api_msql_flask/bilibili_api.py
WorkingDirectory=/opt/bilibili_fans_api_msql_flask/
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable my_bilibili_api_service1.service

sudo tee /etc/systemd/system/my_bilibili_api_service2.service >/dev/null << EOF
[Unit]
Description=My Python Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/bilibili_fans_api_msql_flask/update_bilibili_info.py
WorkingDirectory=/opt/bilibili_fans_api_msql_flask/
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable my_bilibili_api_service2.service

echo '=================='
echo 'bilibili api服务安装完成'
echo '默认开启系统自启服务'
echo '查看状态：'
echo 'sudo systemctl status my_bilibili_api_service1.service'
echo 'sudo systemctl status my_bilibili_api_service2.service'
echo ''
echo '停止服务：'
echo 'sudo systemctl stop my_bilibili_api_service1.service'
echo 'sudo systemctl stop my_bilibili_api_service2.service'
echo ''
echo '重启服务：'
echo 'sudo systemctl restart my_bilibili_api_service1.service'
echo 'sudo systemctl restart my_bilibili_api_service2.service'
echo ''
echo '修改配置文件：'
echo 'sudo vim /opt/bilibili_fans_api_msql_flask/conf.ini'
echo 'sudo vim /opt/bilibili_fans_api_msql_flask/conf.yaml'
echo '=================='
