

import configparser
import time
from tools.GenUserInfo import GetUserInfo

get_user_info = GetUserInfo('conf.ini', 'conf.yaml')

config_ini = configparser.ConfigParser()
config_ini.read('conf.ini', encoding='utf-8')

stat_frequency = config_ini.get('update_frequency', 'stat')
upstat_frequency = config_ini.get('update_frequency', 'upstat')
info_frequency = config_ini.get('update_frequency', 'info')


def update_bilibili_info():
    i = 0
    j = 0
    k = 0
    while True:
        i += 1
        j += 1
        k += 1
        if i % int(stat_frequency) == 0:
            print(f"stat_frequency: {i}")
            get_user_info.main_update_stat()
            i = 0
        if j % int(upstat_frequency) == 0:
            print(f"upstat_frequency: {j}")
            get_user_info.main_update_upstat()
            j = 0
        if k % int(info_frequency) == 0:
            print(f"info_frequency: {k}")
            get_user_info.main_update_info()
            k = 0
        time.sleep(1)


update_bilibili_info()