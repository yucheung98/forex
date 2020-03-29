from flask import Blueprint, render_template, jsonify, request
from .. import connection, logger

login_blue_print = Blueprint('login_blue_print', __name__)

@login_blue_print.route('/login', methods=['POST'])
def login():
    req = request.json
    user_id = req['user_id']
    pwd = req['pwd']
    res = {}
    res1 = {'status': 1, 'user_id': 'sa', 'user_role': 0}
    res2 = {'status': 0}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user"
            cursor.execute(sql)
            result = cursor.fetchall()[0]
            logger.info(result)
            if (user_id == result['user_id']) & (pwd == result['pwd']):
                res = res1
            else:
                res = res2
        connection.commit()
    finally:
        logger.info(res)
    return jsonify(res)


