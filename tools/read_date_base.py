import pymysql
import configparser
import yaml


class ReadDateBase:
    """读取数据库"""

    def __init__(self, config_ini, config_yaml):
        self.config = configparser.ConfigParser()
        self.config.read(config_ini, encoding='utf-8')
        self.conn, self.cursor = self.get_connection()

        with open(config_yaml, 'r', encoding='utf-8') as file:
            self.config_yaml = yaml.safe_load(file)

    def get_connection(self):
        """连接数据库"""
        host = self.config.get('database', 'host')
        port = self.config.getint('database', 'port')
        username = self.config.get('database', 'username')
        password = self.config.get('database', 'password')
        database = self.config.get('database', 'database')
        try:
            conn = pymysql.connect(  # 连接数据库
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
            cursor = conn.cursor()  # 获取游标
            print(f'连接成功...{host}:{port}')
            return conn, cursor
        except pymysql.err.OperationalError as e:
            # 捕获OperationalError异常
            print("报错类型：", type(e))
            print("错误信息：", e)
            conn, cursor = self.create_db(host, username, password)
            print(f"创建数据库!")
            return conn, cursor
        except Exception as e:
            print(f"连接失败 {host}:{port}:{e}")
            return None, None

    # 创建数据库
    def create_db(self, host, user, password):
        database_name = self.config.get('database', 'database')
        conn = pymysql.connect(host=host, user=user, password=password)
        cursor = conn.cursor()
        create_query = f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        cursor.execute(create_query)
        conn.select_db(database_name)   # 切换到新创建的数据库
        return conn, cursor

    # 创建数据表
    def create_sheet(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS stat_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                follower_count TEXT comment '粉丝数',
                following_count TEXT comment '关注数',
                record_time DATETIME comment '记录时间',
                log_text TEXT comment '上次记录的状态日志'
            )
        """
        self.cursor.execute(create_table_query)
        create_table_query = """
            CREATE TABLE IF NOT EXISTS upstat_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                likes TEXT comment '点赞数',
                archive_view TEXT comment '播放数',
                article_view TEXT comment '阅读数',
                record_time DATETIME comment '记录时间',
                log_text TEXT comment '上次记录的状态日志'
            )
        """
        self.cursor.execute(create_table_query)
        create_table_query = """
            CREATE TABLE IF NOT EXISTS info_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_path TEXT comment '用户图像保存路径',
                record_time DATETIME comment '记录时间',
                log_text TEXT comment '上次记录的状态日志'
            )
        """
        self.cursor.execute(create_table_query)

    def insert_info(self, image_path, recoder_time, log_text):
        sql = """
            INSERT INTO `info_data`(`image_path`, `record_time`, `log_text`) 
            VALUES (%s, %s, %s)
        """
        value = (image_path, recoder_time, log_text)
        self.cursor.execute(sql, value)

    def insert_stat(self, follower_count, following_count, recoder_time, log_text):
        sql = """
            INSERT INTO `stat_data`(`follower_count`, `following_count` ,`record_time`, `log_text`) 
            VALUES (%s, %s, %s, %s)
        """
        value = (follower_count, following_count, recoder_time, log_text)
        self.cursor.execute(sql, value)

    def insert_upstat(self, likes, archive_view, article_view, recoder_time, log_text):
        sql = """
            INSERT INTO `upstat_data`(`likes`, `archive_view`, `article_view`, `record_time`, `log_text`) 
            VALUES (%s, %s, %s, %s, %s)
        """
        print((likes, archive_view, article_view, recoder_time, log_text))
        value = (likes, archive_view, article_view, recoder_time, log_text)
        self.cursor.execute(sql, value)

    def show(self):
        # 获取数据库的表名
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        print(f"tables:\n{tables}")

    def end(self):
        # 提交事务
        self.conn.commit()
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
        print(f"结束连接！")


def main():
    """ 要调用end()函数, 才能起效"""
    read_date_base = ReadDateBase('conf.ini', 'conf.yaml')
    read_date_base.create_sheet()
    read_date_base.show()
    read_date_base.end()


if __name__ == '__main__':
    main()
