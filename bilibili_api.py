from flask import Flask, jsonify
from tools.GenUserInfo import GetUserInfo

app = Flask(__name__)
get_user_info = GetUserInfo('conf.ini', 'conf.yaml')


@app.route("/bilibili/update/all", methods=["POST", 'GET'])
def bilibili_update_all():
    """
    :return:
    """
    try:
        update_time, update_data = get_user_info.main_update_all()
        return jsonify(msg="更新成功", update_time=update_time, update_data=update_data)
    except Exception as e:
        print(e)
        return jsonify(msg=f"更新失败 {e}")


@app.route("/bilibili/update/stat", methods=["POST", 'GET'])
def bilibili_update_stat():
    """
    :return:
    """
    try:
        update_time, update_data = get_user_info.main_update_stat()
        return jsonify(msg="更新成功", update_time=update_time, update_data=update_data)
    except Exception as e:
        print(e)
        return jsonify(msg=f"更新失败 {e}")


@app.route("/bilibili/update/upstat", methods=["POST", 'GET'])
def bilibili_update_upstat():
    """
    uid: 你的uid
    :return:
    """
    try:
        update_time, update_data = get_user_info.main_update_upstat()
        return jsonify(msg="更新成功", update_time=update_time, update_data=update_data)
    except Exception as e:
        print(e)
        return jsonify(msg=f"更新失败 {e}")


@app.route("/bilibili/update/info", methods=["POST", 'GET'])
def bilibili_update_info():
    """
    uid: 你的uid
    :return:
    """
    try:
        update_time, update_data = get_user_info.main_update_info()
        return jsonify(msg="更新成功", update_time=update_time, update_data=update_data)
    except Exception as e:
        print(e)
        return jsonify(msg=f"更新失败 {e}")


@app.route("/bilibili/fans", methods=["POST", 'GET'])
def bilibili_fans():
    """
    uid: 你的uid
    :return:
    """

    # get_data = request.get_json()
    # uid = get_data.get("uid")
    #
    # if not all([uid]):
    #     return jsonify(msg="参数不完整")

    fans_num, record_time = get_user_info.main_gen_fans_from_db()
    return jsonify(fans_num=fans_num, record_time=record_time)


if __name__ == '__main__':
    app.run(host="0.0.0.0")  # host="0.0.0.0")使任何主机都能访问

