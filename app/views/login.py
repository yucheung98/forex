from flask import Blueprint, jsonify, request
from .. import config, logger
import pymysql

login_blue_print = Blueprint('login_blue_print', __name__)

@login_blue_print.route('/login', methods=['POST'])
def login():
    req = request.json
    user_name = req['user_name']
    pwd = req['pwd']
    res = {}
    res1 = {'status': 1, 'user_name': 'sa', 'user_role': 0}
    res2 = {'status': 0}
    # Connect to the database
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE user_role = 0"
            cursor.execute(sql)
            result = cursor.fetchall()[0]
            logger.info(result)
            if (user_name == result['user_name']) & (pwd == result['pwd']):
                res = res1
            else:
                res = res2
        connection.commit()
    finally:
        logger.info(res)
        connection.close()
    return jsonify(res)

@login_blue_print.route('/login_2', methods=['POST'])
def login_2():
    req = request.json
    user_name = req['user_name']
    pwd = req['pwd']
    res = {}
    res1 = {'status': 1, 'user_name': ''}
    res2 = {'status': 0}
    # Connect to the database
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `user` WHERE `user_name` = %s"
            cursor.execute(sql, user_name)
            result = cursor.fetchall()[0]
            logger.info(result)
            if (user_name == result['user_name']) & (pwd == result['pwd']):
                res1['user_name'] = user_name
                res = res1
            else:
                res = res2
        connection.commit()
    finally:
        logger.info(res)
        connection.close()
    return jsonify(res)

@login_blue_print.route('/register', methods=['POST'])
def register():
    req = request.json
    user_name = req['user_name']
    pwd = req['pwd']
    res = {}
    # Connect to the database
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `user` (`user_name`, `pwd`, `user_role`) VALUES (%s, %s, 1)"
            cursor.execute(sql, (user_name, pwd))
            res = {'status': 1}
        connection.commit()
    finally:
        connection.close()
    return jsonify(res)

@login_blue_print.route('/get_user_data', methods=['GET'])
def get_user_data():
    res = {}
    # Connect to the database
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user"
            cursor.execute(sql)
            result = cursor.fetchall()
            logger.info(result)
            res = result
        connection.commit()
    finally:
        logger.info(res)
        connection.close()
    return jsonify(res)

@login_blue_print.route('/delete_user', methods=['POST'])
def delete_user():
    req = request.json
    user_id = req['user_id']
    res = {}
    res1 = {'status': 1}
    res2 = {'status': 0}
    # Connect to the database
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM user WHERE user_id = %s"
            cursor.execute(sql, user_id)
            res = res1
        connection.commit()
    finally:
        logger.info(res)
        connection.close()
    return jsonify(res)