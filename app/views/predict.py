from flask import Blueprint, jsonify, request
# from keras.models import load_model
import numpy as np
import pandas as pd
import pymysql
from .. import config, logger, symbols_main

predict_blue_print = Blueprint('predict_blue_print', __name__)

@predict_blue_print.route('/predict')
def predict():
    # Connect to the database
    connection = pymysql.connect(**config)
    # res = {'status': 1, "message": 'ok', 'data': []}
    # try:
    #     with connection.cursor() as cursor:
    #         sql = "select `close` from `EURUSD_D1` order by id desc limit 0,10"
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         x_list = []
    #         for i in result:
    #             x_list.append(i['close'])
    #     connection.commit()
    #     model = load_model('model.h5')  # 载入程序所在目录下名为model的h5模型框架参数
    #     data_x = np.array(x_list).reshape(1, 10, 1)
    #     # print(x_list)
    #     # print(data_x.shape)
    #     y_pred = model.predict(data_x, batch_size=1)
    #     x_list.append(float(format(y_pred.tolist()[0][0], '.5f')))
    #     res["data"] = x_list
    # finally:
    #     connection.close()
    return jsonify(res)