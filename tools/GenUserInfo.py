"""
获取用户信息：
    图像路径
    粉丝数
    点赞数
    播放数
"""
import os.path
import requests
import json
import datetime
import configparser
import yaml
from tools.read_date_base import ReadDateBase


class ProcessDatabase(ReadDateBase):
    def __init__(self, config_ini, config_yaml):
        super().__init__(config_ini, config_yaml)
        self.create_sheet()

    def get_fans(self):
        # 查询最新日期
        query_latest_date = "SELECT MAX(record_time) FROM stat_data"
        self.cursor.execute(query_latest_date)
        latest_date = self.cursor.fetchone()[0]

        # 查询follower字段数据
        query_follower_data = f"SELECT follower_count FROM stat_data WHERE record_time = '{latest_date}'"
        self.cursor.execute(query_follower_data)
        follower_data = self.cursor.fetchall()[0][0]

        return follower_data, latest_date


class GetUserInfo:
    def __init__(self, config_ini, config_yaml):
        # 读取配置文件
        self.config_ini= configparser.ConfigParser()
        self.config_ini.read(config_ini, encoding='utf-8')

        with open(config_yaml, 'r', encoding='utf-8') as file:
            self.config_yaml = yaml.safe_load(file)

        self.uid = 353300793
        self.user_info = {
            "uid": self.uid,
            "follower": 'null',         # 粉丝数
            "following": 'null',        # 关注数
            "recoder_time_1": 'null',   # 粉丝数、关注数的记录时间
            "log_1": 'null',            # 粉丝数、关注数的日志
            "likes": 'null',            # 点赞数
            "archive_view": 'null',     # 播放数
            "article_view": 'null',     # 阅读数
            "recoder_time_2": 'null',   # 点赞数、阅读数、播放数的记录时间
            "log_2": 'null',            # 粉丝数、关注数的日志
            "image_path": 'null',        # 头像
            "recoder_time_3": 'null',   # 头像的记录时间
            "log_3": 'null',            # 粉丝数、关注数的日志
        }

        # 获取api
        self.stat_api = self.process_api_str([self.config_yaml['api']['stat_api'][key] for key in self.config_yaml['api']['stat_api']])
        self.info_api = self.process_api_str(self.config_yaml['api']['info_api'][key] for key in self.config_yaml['api']['info_api'])
        self.upstat_api = self.process_api_str(self.config_yaml['api']['upstat_api'][key] for key in self.config_yaml['api']['upstat_api'])
        print(self.stat_api, '\n', self.info_api, '\n', self.upstat_api)

        # 请求头
        self.headers = self.config_yaml['browser_request_data']['headers']

        # 用户文件
        self.root = self.config_ini.get('user_files', 'root')
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        self.face_img = os.path.join(self.root, 'img')
        if not os.path.exists(self.face_img):
            os.makedirs(self.face_img)

        self.process_database = ProcessDatabase(config_ini, config_yaml)

    def process_api_str(self, str_list):
        """
        将yaml配置文件中的api字符串合并并转换为一个url
        :param str_list:
        :return:
        """
        str_ = ''.join(str_list)
        if 'UID' in str_:
            api_str = str_.replace('UID', str(self.uid))
        else:
            api_str = str_
        return api_str

    def download_image(self, img_url):
        """下载图像"""
        try:
            response = requests.get(img_url)
            response.raise_for_status()
            image_name = f"face_{self.user_info['uid']}.jpg"
            save_path = os.path.join(self.face_img, image_name)
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"图像下载成功！ save to: {save_path}")
            return save_path
        except Exception as e:
            print(f"图像下载失败:", str(e))

    def update_stat_api_request_data(self):
        """
        更新stat_api请求数据

        :return:
        """
        try:
            response = requests.get(self.stat_api, headers=self.headers)
            json_data = response.json()
            # print(json_data)  # --测试代码--
            if json_data['code'] == (-412 or -504):   # 请求被拦截, {"code":-412,"message":"请求被拦截","ttl":1,"data":null}
                self.user_info["recoder_time_1"] = str(datetime.datetime.now())[:19]
                self.user_info["log_1"] = f"{str(datetime.datetime.now())[:19]}: 请求错误: code is {json_data['code']}, message is {json_data['message']}"
            elif json_data['data'] == {}:
                self.user_info["log_1"] = f"{str(datetime.datetime.now())[:19]}: 请求异常: data is none"
            else:
                self.user_info["following"] = json_data['data']['following']  # 关注数
                self.user_info["follower"] = json_data['data']['follower']  # 粉丝数
                self.user_info["log_1"] = "ok"
                self.user_info["recoder_time_1"] = str(datetime.datetime.now())[:19]  # 当前系统时间,提取前19位, 如 2022-03-28 16:03:59
        except IOError as e:
            self.user_info["recoder_time_1"] = str(datetime.datetime.now())[:19]
            self.user_info["log_1"] = f"{str(datetime.datetime.now())[:19]}: 网络错误, 请关闭代理后重试！{e}"
        except Exception as e:
            self.user_info["recoder_time_1"] = str(datetime.datetime.now())[:19]
            self.user_info["log_1"] = f"{str(datetime.datetime.now())[:19]}: 未知错误, 请联系开发者！{e}"

    def update_upstat_api_request_data(self):
        """
        更新upstat_api请求数据

        :return:
        """
        try:
            response = requests.get(self.upstat_api, headers=self.headers)
            json_data = response.json()
            # print(json_data)  # --测试代码--
            if json_data['code'] == (-412 or -504):   # 请求被拦截, {"code":-412,"message":"请求被拦截","ttl":1,"data":null}
                self.user_info["recoder_time_2"] = str(datetime.datetime.now())[:19]
                self.user_info["log_2"] = f"{str(datetime.datetime.now())[:19]}: 请求错误: code is {json_data['code']}, message is {json_data['message']}"
            elif json_data['data'] == {}:
                self.user_info["recoder_time_2"] = str(datetime.datetime.now())[:19]
                self.user_info["log_2"] = f"{str(datetime.datetime.now())[:19]}: 请求异常: data is none"
            else:
                self.user_info["likes"] = json_data['data']['likes']  # 点赞数
                self.user_info["archive_view"] = json_data['data']['archive']['view']  # 粉播放数
                self.user_info["article_view"] = json_data['data']['article']['view']  # 阅读数
                self.user_info["log_2"] = "ok"
                self.user_info["recoder_time_2"] = str(datetime.datetime.now())[:19]  # 当前系统时间,提取前19位, 如 2022-03-28 16:03:59
        except IOError as e:
            self.user_info["recoder_time_2"] = str(datetime.datetime.now())[:19]
            self.user_info["log_2"] = f"{str(datetime.datetime.now())[:19]}: 网络错误, 请关闭代理后重试！{e}"
        except Exception as e:
            self.user_info["recoder_time_2"] = str(datetime.datetime.now())[:19]
            self.user_info["log_2"] = f"{str(datetime.datetime.now())[:19]}: 未知错误, 请联系开发者！{e}"

    def update_info_api_request_data(self):
        """
        更新info_api请求数据

        :return:
        """
        try:
            response = requests.get(self.info_api, headers=self.headers)
            json_data = response.json()
            print(json_data)  # --测试代码--
            if json_data['code'] == (-412 or -504):   # 请求被拦截, {"code":-412,"message":"请求被拦截","ttl":1,"data":null}
                self.user_info["recoder_time_3"] = str(datetime.datetime.now())[:19]
                self.user_info["log_3"] = f"{str(datetime.datetime.now())[:19]}: 请求错误: code is {json_data['code']}, message is {json_data['message']}"
            elif json_data['data'] == {}:
                self.user_info["recoder_time_3"] = str(datetime.datetime.now())[:19]
                self.user_info["log_3"] = f"{str(datetime.datetime.now())[:19]}: 请求异常: data is none"
            else:
                user_face_url = json_data['data']['face']
                self.user_info['image_path'] = self.download_image(user_face_url)
                self.user_info["log_3"] = "ok"
                self.user_info["recoder_time_3"] = str(datetime.datetime.now())[:19]  # 当前系统时间,提取前19位, 如 2022-03-28 16:03:59
        except IOError as e:
            self.user_info["recoder_time_3"] = str(datetime.datetime.now())[:19]
            self.user_info["log_3"] = f"{str(datetime.datetime.now())[:19]}: 网络错误, 请关闭代理后重试！{e}"
        except Exception as e:
            self.user_info["recoder_time_3"] = str(datetime.datetime.now())[:19]
            self.user_info["log_3"] = f"{str(datetime.datetime.now())[:19]}: 未知错误, 请联系开发者！{e}"

    def main_update_all(self):
        """示例1 更新数据库中的数据"""
        self.update_stat_api_request_data()
        self.update_upstat_api_request_data()
        self.update_info_api_request_data()
        json_str = json.dumps(self.user_info, indent=4, ensure_ascii=False)     # 将JSON数据转换为字符串，并设置缩进参数indent=4
        print(json_str)
        # 将新数据写入数据库
        self.process_database.insert_stat(self.user_info['follower'],
                                          self.user_info['following'],
                                          self.user_info['recoder_time_1'],
                                          self.user_info['log_1'])
        self.process_database.insert_upstat(self.user_info['likes'],
                                            self.user_info['archive_view'],
                                            self.user_info['article_view'],
                                            self.user_info['recoder_time_2'],
                                            self.user_info['log_2'])
        self.process_database.insert_info(self.user_info['image_path'],
                                          self.user_info['recoder_time_3'],
                                          self.user_info['log_3'])
        self.process_database.conn.commit()
        # 返回数据
        update_time = self.user_info['recoder_time_1']
        update_data = {'follower': self.user_info['follower'],
                       'following': self.user_info['following'],
                       'recoder_time_1': self.user_info['recoder_time_1'],
                       'log_1': self.user_info['log_1'],
                       'likes': self.user_info['likes'],
                       'archive_view': self.user_info['archive_view'],
                       'article_view': self.user_info['article_view'],
                       'recoder_time_2': self.user_info['recoder_time_2'],
                       'log_2': self.user_info['log_2'],
                       'image_path': self.user_info['image_path'],
                       'recoder_time_3': self.user_info['recoder_time_3'],
                       'log_3': self.user_info['log_3']}
        return update_time, update_data

    def main_update_stat(self):
        """示例1 更新数据库中的数据"""
        self.update_stat_api_request_data()
        json_str = json.dumps(self.user_info, indent=4, ensure_ascii=False)     # 将JSON数据转换为字符串，并设置缩进参数indent=4
        print(json_str)
        # 将新数据写入数据库
        self.process_database.insert_stat(self.user_info['follower'],
                                          self.user_info['following'],
                                          self.user_info['recoder_time_1'],
                                          self.user_info['log_1'])
        self.process_database.conn.commit()
        # 返回数据
        update_time = self.user_info['recoder_time_1']
        update_data = {'follower': self.user_info['follower'],
                       'following': self.user_info['following'],
                       'recoder_time_1': self.user_info['recoder_time_1'],
                       'log_1': self.user_info['log_1']}
        return update_time, update_data

    def main_update_upstat(self):
        """示例1 更新数据库中的数据"""
        self.update_upstat_api_request_data()
        json_str = json.dumps(self.user_info, indent=4, ensure_ascii=False)     # 将JSON数据转换为字符串，并设置缩进参数indent=4
        print(json_str)
        # 将新数据写入数据库
        self.process_database.insert_upstat(self.user_info['likes'],
                                            self.user_info['archive_view'],
                                            self.user_info['article_view'],
                                            self.user_info['recoder_time_2'],
                                            self.user_info['log_2'])
        self.process_database.conn.commit()
        # 返回数据
        update_time = self.user_info['recoder_time_1']
        update_data = {'likes': self.user_info['likes'],
                       'archive_view': self.user_info['archive_view'],
                       'article_view': self.user_info['article_view'],
                       'recoder_time_2': self.user_info['recoder_time_2'],
                       'log_2': self.user_info['log_2']}
        return update_time, update_data

    def main_update_info(self):
        """示例1 更新数据库中的数据"""
        self.update_info_api_request_data()
        json_str = json.dumps(self.user_info, indent=4, ensure_ascii=False)     # 将JSON数据转换为字符串，并设置缩进参数indent=4
        print(json_str)
        # 将新数据写入数据库
        self.process_database.insert_info(self.user_info['image_path'],
                                          self.user_info['recoder_time_3'],
                                          self.user_info['log_3'])
        self.process_database.conn.commit()
        # 返回数据
        update_time = self.user_info['recoder_time_1']
        update_data = {'image_path': self.user_info['image_path'],
                       'recoder_time_3': self.user_info['recoder_time_3'],
                       'log_3': self.user_info['log_3']}
        return update_time, update_data

    def main_gen_fans(self):
        """示例2 获取粉丝数"""
        fans = self.user_info['follower']
        print(f"fans:{fans}")
        return fans

    def main_gen_fans_from_db(self):
        """示例3 从数据库获取粉丝数"""
        fans, record_time = self.process_database.get_fans()
        print(f"fans:{fans}")
        return fans, record_time


if __name__ == '__main__':
    get_user_info = GetUserInfo('../conf.ini', '../conf.yaml')
    # get_user_info.update_all()
    # get_user_info.gen_fans()
    # get_user_info.gen_fans_from_db()

    # get_user_info.main_update_stat()
    # get_user_info.main_update_upstat()
    get_user_info.main_update_info()



