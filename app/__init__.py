# coding=utf-8
from flask import Flask
from flask_cors import CORS
import pymysql
import logging

config = {
    'host': '116.196.90.212',
    'port': 3306,
    'user': 'root',
    'password': '0000',
    'db': 'forex',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
# Connect to the database
connection = pymysql.connect(**config)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    # 将蓝图程序与app关联到一起，这样使app识别蓝图程序中的路由
    from .views.login import login_blue_print
    app.register_blueprint(login_blue_print)
    return app

