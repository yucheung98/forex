# coding=utf-8
from flask import Flask
from flask_cors import CORS
import pymysql
import logging

config = {
    'host': '123.56.134.7',
    'port': 3306,
    'user': 'root',
    'password': '0000',
    'db': 'forex',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

symbols_main = ['EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD', 'USDCHF', 'USDCAD']
symbols_list = ['EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCNH', 'USDRUB', 'AUDUSD', 'NZDUSD', 'USDCAD', 'USDSEK', 'USDHKD', 'USDSGD',
                'USDNOK', 'USDDKK', 'USDTRY', 'USDZAR', 'USDCZK', 'USDHUF', 'USDPLN', 'USDRUR', 'AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD',
                'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURCZK', 'EURDKK', 'EURGBP', 'EURHKD', 'EURHUF', 'EURJPY',
                'EURNOK', 'EURNZD', 'EURPLN', 'EURRUR', 'EURRUB', 'EURSEK', 'EURTRY', 'EURZAR', 'GBPAUD', 'GBPCHF', 'GBPJPY', 'XAUUSD',
                'XAGUSD', 'GBPCAD', 'GBPNOK', 'GBPNZD', 'GBPPLN', 'GBPSEK', 'GBPSGD', 'GBPZAR', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDSGD',
                'SGDJPY', 'USDGEL', 'USDMXN', 'EURMXN', 'GBPMXN', 'CADMXN', 'CHFMXN', 'MXNJPY', 'NZDMXN', 'USDCOP', 'USDARS', 'USDCLP']

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    # 将蓝图程序与app关联到一起，这样使app识别蓝图程序中的路由
    from .views.login import login_blue_print
    app.register_blueprint(login_blue_print)
    from .views.quotations import quotations_blue_print
    app.register_blueprint(quotations_blue_print)
    from .views.news import news_blue_print
    app.register_blueprint(news_blue_print)
    from .views.predict import predict_blue_print
    app.register_blueprint(predict_blue_print)
    return app

