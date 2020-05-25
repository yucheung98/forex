from flask import Blueprint, jsonify, request
from keras.models import load_model
import numpy as np
import pandas as pd
import pymysql, datetime
from .. import config, logger, symbols_main
from keras import backend as K

predict_blue_print = Blueprint('predict_blue_print', __name__)

@predict_blue_print.route('/predict')
def predict():
    symbol_pred = ['EURUSD', 'USDJPY', 'GBPUSD']
    # Connect to the database
    connection = pymysql.connect(**config)
    res = {'status': 1, "message": 'ok', 'data': {'EURUSD': [], 'USDJPY': [], 'GBPUSD': []}}
    EURUSD_max = 1.39304
    EURUSD_min = 1.03867
    USDJPY_mean = 107.86830746
    USDJPY_std = 9.37805123
    GBPUSD_max = 1.71626
    GBPUSD_min = 1.1465299999999998

    # EURUSD预测
    try:
        with connection.cursor() as cursor:
            sql = "select `close` from `D1` WHERE symbol = 'EURUSD' order by id desc limit 0,10"
            cursor.execute(sql)
            result = cursor.fetchall()
            x_list_origin = []
            x_list = []
            for i in range(len(result)):
                x_list_origin.append(result[9 - i]['close'])
                x_list.append((result[9 - i]['close'] - EURUSD_min)*(EURUSD_max - EURUSD_min))
        connection.commit()
        model = load_model('EURUSD_pre_model.h5')  # 载入程序所在目录下名为model的h5模型框架参数
        data_x = np.array(x_list).reshape(1, 10, 1)
        y_pred = model.predict(data_x, batch_size=1)
        x_list_origin.append(float(format(y_pred.tolist()[0][0] *(EURUSD_max - EURUSD_min) + EURUSD_min, '.5f')))
        res["data"]["EURUSD"] = x_list_origin
        # 更新预测结果
        cursor = connection.cursor()
        sql2 = "UPDATE `pred_result` set `close_1` = %s, `close_2` = %s, `close_3` = %s, `close_4` = %s, `close_5` = %s, `close_6` = %s, `close_7` = %s, `close_8` = %s, `close_9` = %s, `close_10` = %s, `close_pred` = %s WHERE symbol = 'EURUSD'"
        cursor.execute(sql2, (x_list_origin[0], x_list_origin[1], x_list_origin[2], x_list_origin[3], x_list_origin[4], x_list_origin[5], x_list_origin[6], x_list_origin[7], x_list_origin[8], x_list_origin[9], x_list_origin[10]))
        connection.commit()
    finally:
        K.clear_session()
        print("EURUSD      pred     ok!")


    # USDJPY预测
    try:
        with connection.cursor() as cursor:
            sql = "select `close` from `D1` WHERE symbol = 'USDJPY' order by id desc limit 0,10"
            cursor.execute(sql)
            result = cursor.fetchall()
            x_list_origin = []
            x_list = []
            for i in range(len(result)):
                x_list_origin.append(result[9 - i]['close'])
                x_list.append((result[9 - i]['close'] - USDJPY_mean)/USDJPY_std)
        connection.commit()
        model = load_model('USDJPY_pre_model.h5')  # 载入程序所在目录下名为model的h5模型框架参数
        data_x = np.array(x_list).reshape(1, 10, 1)
        y_pred = model.predict(data_x, batch_size=1)
        x_list_origin.append(float(format(y_pred.tolist()[0][0] * USDJPY_std + USDJPY_mean, '.3f')))
        res["data"]["USDJPY"] = x_list_origin
        # 更新预测结果
        cursor = connection.cursor()
        sql2 = "UPDATE `pred_result` set `close_1` = %s, `close_2` = %s, `close_3` = %s, `close_4` = %s, `close_5` = %s, `close_6` = %s, `close_7` = %s, `close_8` = %s, `close_9` = %s, `close_10` = %s, `close_pred` = %s WHERE symbol = 'USDJPY'"
        cursor.execute(sql2, (
        x_list_origin[0], x_list_origin[1], x_list_origin[2], x_list_origin[3], x_list_origin[4], x_list_origin[5],
        x_list_origin[6], x_list_origin[7], x_list_origin[8], x_list_origin[9], x_list_origin[10]))
        connection.commit()
    finally:
        K.clear_session()
        print("USDJPY      pred     ok!")

    # GBPUSD预测
    try:
        with connection.cursor() as cursor:
            sql = "select `close` from `D1` WHERE symbol = 'GBPUSD' order by id desc limit 0,10"
            cursor.execute(sql)
            result = cursor.fetchall()
            x_list_origin = []
            x_list = []
            for i in range(len(result)):
                x_list_origin.append(result[9 - i]['close'])
                x_list.append((result[9 - i]['close'] - GBPUSD_min) * (GBPUSD_max - GBPUSD_min))
        connection.commit()
        model = load_model('GBPUSD_pre_model.h5')  # 载入程序所在目录下名为model的h5模型框架参数
        data_x = np.array(x_list).reshape(1, 10, 1)
        y_pred = model.predict(data_x, batch_size=1)
        x_list_origin.append(float(format(y_pred.tolist()[0][0] * (GBPUSD_max - GBPUSD_min) + GBPUSD_min, '.5f')))
        res["data"]["GBPUSD"] = x_list_origin
        # 更新预测结果
        cursor = connection.cursor()
        sql2 = "UPDATE `pred_result` set `close_1` = %s, `close_2` = %s, `close_3` = %s, `close_4` = %s, `close_5` = %s, `close_6` = %s, `close_7` = %s, `close_8` = %s, `close_9` = %s, `close_10` = %s, `close_pred` = %s WHERE symbol = 'GBPUSD'"
        cursor.execute(sql2, (
            x_list_origin[0], x_list_origin[1], x_list_origin[2], x_list_origin[3], x_list_origin[4], x_list_origin[5],
            x_list_origin[6], x_list_origin[7], x_list_origin[8], x_list_origin[9], x_list_origin[10]))
        connection.commit()
    finally:
        K.clear_session()
        print("GBPUSD      pred     ok!")

    # 更新时间
    cursor = connection.cursor()
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql3 = "UPDATE `update_time` set `prediction` = %s"
    cursor.execute(sql3, now_time)
    connection.commit()
    connection.close()
    return jsonify(res)


# 备份
# @predict_blue_print.route('/predict', methods=['POST'])
# def predict():
#     req = request.json
#     logger.info(req)
#     symbol = req['symbol']
#     # Connect to the database
#     connection = pymysql.connect(**config)
#     res = {'status': 1, "message": 'ok', 'data': []}
#     EURUSD_max = 1.39304
#     EURUSD_min = 1.03867
#     USDJPY_mean = 107.86830746
#     USDJPY_std = 9.37805123
#     GBPUSD_max = 1.71626
#     GBPUSD_min = 1.1465299999999998
#     try:
#         with connection.cursor() as cursor:
#             sql = "select `close` from `D1` WHERE symbol = %s order by id desc limit 0,10"
#             cursor.execute(sql, symbol)
#             result = cursor.fetchall()
#             x_list_origin = []
#             x_list = []
#             for i in range(len(result)):
#                 x_list_origin.append(result[9 - i]['close'])
#                 x_list.append((result[9 - i]['close'] - 107.86830746)/9.37805123)
#         connection.commit()
#         model = load_model(symbol + '_pre_model.h5')  # 载入程序所在目录下名为model的h5模型框架参数
#         data_x = np.array(x_list).reshape(1, 10, 1)
#         # print(x_list)
#         # print(data_x.shape)
#         y_pred = model.predict(data_x, batch_size=1)
#         x_list_origin.append(float(format(y_pred.tolist()[0][0] * 9.37805123 + 107.86830746, '.3f')))
#         # x_list_origin.append(float(format(float(format(y_pred.tolist()[0][0], '.5f'))*9.37805123 + 107.86830746,  '.3f')))
#         res["data"] = x_list_origin
#     finally:
#         connection.close()
#         K.clear_session()
#     return jsonify(res)

@predict_blue_print.route('/get_predict_result')
def get_predict_result():
    symbol_pred = ['EURUSD', 'USDJPY', 'GBPUSD']
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    res = {'status': 1, "message": 'ok', 'data': {'EURUSD': [], 'USDJPY': [], 'GBPUSD': []}}
    for s in symbol_pred:
        sql = "SELECT * FROM `pred_result` WHERE symbol = %s"
        cursor.execute(sql, s)
        result = cursor.fetchall()[0]
        serie = [result['close_1'], result['close_2'], result['close_3'], result['close_4'], result['close_5'], result['close_6'], result['close_7'], result['close_8'], result['close_9'], result['close_10'], result['close_pred'], ]
        res['data'][s] = serie
    connection.commit()
    connection.close()
    return jsonify(res)