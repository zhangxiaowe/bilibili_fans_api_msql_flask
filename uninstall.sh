#!/bin/bash

sudo systemctl stop my_bilibili_api_service.service
sudo rm -rf /etc/systemd/system/my_bilibili_api_service.service

sudo systemctl daemon-reload

echo '=================='
echo 'bilibili api 服务卸载完成。'
echo '=================='