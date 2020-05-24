from flask import Blueprint, jsonify, request
from .. import config, logger, symbols_main
from datetime import datetime
import MetaTrader5 as mt5
import pymysql

quotations_blue_print = Blueprint('quotations_blue_print', __name__)

# @quotations_blue_print.route('/update_rates_D1')
# def update_rates_D1():
#     res = {'status': 1}
#     # Connect to the database
#     connection = pymysql.connect(**config)
#     cursor = connection.cursor()
#     if not mt5.initialize():
#         print("initialize() failed, error code =", mt5.last_error())
#         quit()
#
#     for s in symbols_main:
#         rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_D1, 1, 60).tolist()
#         if s == 'EURUSD':
#             sql1 = "DELETE FROM `EURUSD_D1`"
#         if s == 'USDJPY':
#             sql1 = "DELETE FROM `USDJPY_D1`"
#         if s == 'GBPUSD':
#             sql1 = "DELETE FROM `GBPUSD_D1`"
#         if s == 'AUDUSD':
#             sql1 = "DELETE FROM `AUDUSD_D1`"
#         if s == 'USDCHF':
#             sql1 = "DELETE FROM `USDCHF_D1`"
#         if s == 'USDCAD':
#             sql1 = "DELETE FROM `USDCAD_D1`"
#         cursor.execute(sql1)
#         for rate in rates:
#             timeStamp = rate[0]
#             dateArray = datetime.fromtimestamp(timeStamp)
#             time = dateArray.strftime("%Y/%m/%d")
#             if s == 'EURUSD':
#                  sql2 = "INSERT INTO `EURUSD_D1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'USDJPY':
#                 sql2 = "INSERT INTO `USDJPY_D1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'GBPUSD':
#                 sql2 = "INSERT INTO `GBPUSD_D1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'AUDUSD':
#                 sql2 = "INSERT INTO `AUDUSD_D1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'USDCHF':
#                 sql2 = "INSERT INTO `USDCHF_D1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'USDCAD':
#                 sql2 = "INSERT INTO `USDCAD_D1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             cursor.execute(sql2, (time, rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]))
#         connection.commit()
#     connection.close()
#     mt5.shutdown()
#     return jsonify(res)
#
# @quotations_blue_print.route('/get_rates_D1')
# def get_rates_D1():
#     # Connect to the database
#     connection = pymysql.connect(**config)
#     res = {'EURUSD': {'categories': [], 'series': []}, 'USDJPY': {'categories': [], 'series': []}, 'GBPUSD': {'categories': [], 'series': []},
#            'AUDUSD': {'categories': [], 'series': []}, 'USDCHF': {'categories': [], 'series': []}, 'USDCAD': {'categories': [], 'series': []}}
#     with connection.cursor() as cursor:
#         for s in symbols_main:
#             if s == 'EURUSD':
#                 sql = "SELECT * FROM `EURUSD_D1`"
#             if s == 'USDJPY':
#                 sql = "SELECT * FROM `USDJPY_D1`"
#             if s == 'GBPUSD':
#                 sql = "SELECT * FROM `GBPUSD_D1`"
#             if s == 'AUDUSD':
#                 sql = "SELECT * FROM `AUDUSD_D1`"
#             if s == 'USDCHF':
#                 sql = "SELECT * FROM `USDCHF_D1`"
#             if s == 'USDCAD':
#                 sql = "SELECT * FROM `USDCAD_D1`"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             for r in result:
#                 res[s]['categories'].append(r['time'])
#                 serie = [r['open'], r['close'], r['low'], r['high']]
#                 res[s]['series'].append(serie)
#     connection.commit()
#     connection.close()
#     return jsonify(res)

# 更新所有货币对D1周期数据
# 尝试更新D1周期所有货币对数据
@quotations_blue_print.route('/update_rates_D1')
def update_rates_D1():
    res = {'status': 1}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    # 删除之前的D1数据
    sql1 = "DELETE FROM `D1`"
    cursor.execute(sql1)

    for s in symbols_main:
        rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_D1, 0, 60).tolist()

        for rate in rates:
            timeStamp = rate[0]
            dateArray = datetime.fromtimestamp(timeStamp)
            time = dateArray.strftime("%Y/%m/%d")
            sql2 = "INSERT INTO `D1` (`symbol`, `time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql2, (s, time, rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]))

        connection.commit()
        print(s)
    connection.close()
    mt5.shutdown()
    return jsonify(res)

# 按货币对获取rates_D1
@quotations_blue_print.route('/get_rates_D1', methods=['POST'])
def get_rates_D1():
    req = request.json
    logger.info(req)
    symbol = req['symbol']
    # Connect to the database
    connection = pymysql.connect(**config)
    res = {symbol: {'categories': [], 'series': []}}
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `D1` WHERE symbol = %s"
        cursor.execute(sql, symbol)
        result = cursor.fetchall()
        for r in result:
            res[symbol]['categories'].append(r['time'])
            serie = [r['open'], r['close'], r['low'], r['high']]
            res[symbol]['series'].append(serie)
    connection.commit()
    connection.close()
    return jsonify(res)

@quotations_blue_print.route('/web_get_rates_D1')
def web_get_rates_D1():
    res = {'EURUSD': [], 'USDJPY': [],'GBPUSD': [],'AUDUSD': [], 'USDCHF': [], 'USDCAD': []}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    for s in symbols_main:
        sql = "SELECT * FROM `D1` WHERE symbol = %s"
        cursor.execute(sql, s)
        result = cursor.fetchall()
        res[s] = result
    connection.commit()
    connection.close()
    return jsonify(res)


# @quotations_blue_print.route('/update_rates_H1')
# def update_rates_H1():
#     res = {'status': 1}
#     # Connect to the database
#     connection = pymysql.connect(**config)
#     cursor = connection.cursor()
#     if not mt5.initialize():
#         print("initialize() failed, error code =", mt5.last_error())
#         quit()
#
#     for s in symbols_main:
#         rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_H1, 0, 60).tolist()
#         if s == 'EURUSD':
#             sql1 = "DELETE FROM `EURUSD_H1`"
#         if s == 'USDJPY':
#             sql1 = "DELETE FROM `USDJPY_H1`"
#         if s == 'GBPUSD':
#             sql1 = "DELETE FROM `GBPUSD_H1`"
#         if s == 'AUDUSD':
#             sql1 = "DELETE FROM `AUDUSD_H1`"
#         if s == 'USDCHF':
#             sql1 = "DELETE FROM `USDCHF_H1`"
#         if s == 'USDCAD':
#             sql1 = "DELETE FROM `USDCAD_H1`"
#         cursor.execute(sql1)
#         for rate in rates:
#             timeStamp = rate[0]
#             dateArray = datetime.fromtimestamp(timeStamp)
#             time = dateArray.strftime("%Y/%m/%d  %H:%M:%S")
#             if s == 'EURUSD':
#                  sql2 = "INSERT INTO `EURUSD_H1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'USDJPY':
#                 sql2 = "INSERT INTO `USDJPY_H1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'GBPUSD':
#                 sql2 = "INSERT INTO `GBPUSD_H1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'AUDUSD':
#                 sql2 = "INSERT INTO `AUDUSD_H1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'USDCHF':
#                 sql2 = "INSERT INTO `USDCHF_D1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             if s == 'USDCAD':
#                 sql2 = "INSERT INTO `USDCAD_H1` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#             cursor.execute(sql2, (time, rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]))
#         connection.commit()
#     connection.close()
#     mt5.shutdown()
#     return jsonify(res)
#
# @quotations_blue_print.route('/get_rates_H1')
# def get_rates_H1():
#     # Connect to the database
#     connection = pymysql.connect(**config)
#     res = {'EURUSD': {'categories': [], 'series': []}, 'USDJPY': {'categories': [], 'series': []}, 'GBPUSD': {'categories': [], 'series': []},
#            'AUDUSD': {'categories': [], 'series': []}, 'USDCHF': {'categories': [], 'series': []}, 'USDCAD': {'categories': [], 'series': []}}
#     with connection.cursor() as cursor:
#         for s in symbols_main:
#             if s == 'EURUSD':
#                 sql = "SELECT * FROM `EURUSD_H1`"
#             if s == 'USDJPY':
#                 sql = "SELECT * FROM `USDJPY_H1`"
#             if s == 'GBPUSD':
#                 sql = "SELECT * FROM `GBPUSD_H1`"
#             if s == 'AUDUSD':
#                 sql = "SELECT * FROM `AUDUSD_H1`"
#             if s == 'USDCHF':
#                 sql = "SELECT * FROM `USDCHF_H1`"
#             if s == 'USDCAD':
#                 sql = "SELECT * FROM `USDCAD_H1`"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#             for r in result:
#                 res[s]['categories'].append(r['time'])
#                 serie = [r['open'], r['close'], r['low'], r['high']]
#                 res[s]['series'].append(serie)
#     connection.commit()
#     connection.close()
#     return jsonify(res)

@quotations_blue_print.route('/web_get_rates_H1')
def web_get_rates_H1():
    res = {'EURUSD': [], 'USDJPY': [],'GBPUSD': [],'AUDUSD': [], 'USDCHF': [], 'USDCAD': []}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    for s in symbols_main:
        sql = "SELECT * FROM `H1` WHERE symbol = %s"
        cursor.execute(sql, s)
        result = cursor.fetchall()
        res[s] = result
    connection.commit()
    connection.close()
    return jsonify(res)

# 更新所有货币对H1周期数据
# 尝试更新H1周期所有货币对数据
@quotations_blue_print.route('/update_rates_H1')
def update_rates_H1():
    res = {'status': 1}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    # 删除之前的H1数据
    sql1 = "DELETE FROM `H1`"
    cursor.execute(sql1)

    for s in symbols_main:
        rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_H1, 0, 60).tolist()

        for rate in rates:
            timeStamp = rate[0]
            dateArray = datetime.fromtimestamp(timeStamp)
            time = dateArray.strftime("%Y/%m/%d  %H:%M:%S")
            sql2 = "INSERT INTO `H1` (`symbol`, `time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql2, (s, time, rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]))

        connection.commit()
        print(s)
    connection.close()
    mt5.shutdown()
    return jsonify(res)

# 按货币对获取rates_D1
@quotations_blue_print.route('/get_rates_H1', methods=['POST'])
def get_rates_H1():
    req = request.json
    logger.info(req)
    symbol = req['symbol']
    # Connect to the database
    connection = pymysql.connect(**config)
    res = {symbol: {'categories': [], 'series': []}}
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `H1` WHERE symbol = %s"
        cursor.execute(sql, symbol)
        result = cursor.fetchall()
        for r in result:
            res[symbol]['categories'].append(r['time'])
            serie = [r['open'], r['close'], r['low'], r['high']]
            res[symbol]['series'].append(serie)
    connection.commit()
    connection.close()
    return jsonify(res)

# 获取实时行情
@quotations_blue_print.route('/get_quot_now')
def get_quot_now():
    res = {}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    sql = "SELECT * FROM `quot_now`"
    cursor.execute(sql)
    result = cursor.fetchall()
    res = result
    connection.commit()
    connection.close()
    return jsonify(res)

# 获取用户关注
@quotations_blue_print.route('/get_user_collect', methods=['POST'])
def get_user_collect():
    req = request.json
    user_name = req['user_name']
    res = {'marketList_collect': [], 'collect_list': []}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    sql = "SELECT `symbol` FROM `collect` WHERE `user_name` = %s"
    cursor.execute(sql, user_name)
    result = cursor.fetchall()
    collect_list = []
    i = 0
    for i in range(len(result)):
        collect_list.append(result[i]['symbol'])

    collects = "'" + "','".join(str(x) for x in collect_list) + "'"
    sql2 = "SELECT * FROM quot_now WHERE SYMBOL IN (" + collects +')'
    print(sql2)
    cursor.execute(sql2)

    result2 = cursor.fetchall()

    res['marketList_collect'] = result2
    res['collect_list'] = collect_list

    connection.commit()
    connection.close()
    return jsonify(res)

# 添加关注
@quotations_blue_print.route('/add_collect', methods=['POST'])
def add_collect():
    req = request.json
    logger.info(req)
    user_name = req['user_name']
    symbol = req['symbol']
    res = {'status': 1 ,'marketList_collect': [], 'collect_list': []}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    sql = "INSERT INTO `collect` (`user_name`, `symbol`) VALUES (%s, %s)"
    cursor.execute(sql, (user_name, symbol))

    sql2 = "SELECT `symbol` FROM `collect` WHERE `user_name` = %s"
    cursor.execute(sql2, user_name)
    result = cursor.fetchall()
    collect_list = []
    i = 0
    for i in range(len(result)):
        collect_list.append(result[i]['symbol'])

    collects = "'" + "','".join(str(x) for x in collect_list) + "'"
    sql3 = "SELECT * FROM quot_now WHERE SYMBOL IN (" + collects +')'
    cursor.execute(sql3)

    result2 = cursor.fetchall()

    res['marketList_collect'] = result2
    res['collect_list'] = collect_list

    connection.commit()
    connection.close()
    return jsonify(res)

# 取消关注
@quotations_blue_print.route('/del_collect', methods=['POST'])
def del_collect():
    req = request.json
    logger.info(req)
    user_name = req['user_name']
    symbol = req['symbol']
    res = {'status': 1 ,'marketList_collect': [], 'collect_list': []}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    sql = "DELETE FROM `collect` WHERE `user_name`= %s AND `symbol`= %s"
    cursor.execute(sql, (user_name, symbol))

    sql2 = "SELECT `symbol` FROM `collect` WHERE `user_name` = %s"
    cursor.execute(sql2, user_name)
    result = cursor.fetchall()
    collect_list = []
    i = 0
    for i in range(len(result)):
        collect_list.append(result[i]['symbol'])

    collects = "'" + "','".join(str(x) for x in collect_list) + "'"
    sql3 = "SELECT * FROM quot_now WHERE SYMBOL IN (" + collects +')'
    cursor.execute(sql3)
    result2 = cursor.fetchall()

    res['marketList_collect'] = result2
    res['collect_list'] = collect_list

    connection.commit()
    connection.close()
    return jsonify(res)

# 尝试更新十分钟周期所有货币对数据
@quotations_blue_print.route('/update_rates_M10')
def update_rates_M10():
    res = {'status': 1}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    # 删除之前的M10数据
    sql1 = "DELETE FROM `M10`"
    cursor.execute(sql1)

    for s in symbols_main:
        rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_M10, 0, 60).tolist()

        for rate in rates:
            timeStamp = rate[0]
            dateArray = datetime.fromtimestamp(timeStamp)
            time = dateArray.strftime("%Y/%m/%d  %H:%M:%S")
            sql2 = "INSERT INTO `M10` (`symbol`, `time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql2, (s, time, rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]))

        connection.commit()
        print(s)
    connection.close()
    mt5.shutdown()
    return jsonify(res)

# 按货币对获取rates
@quotations_blue_print.route('/get_rates_M10', methods=['POST'])
def get_rates_M10():
    req = request.json
    logger.info(req)
    symbol = req['symbol']
    # Connect to the database
    connection = pymysql.connect(**config)
    res = {symbol: {'categories': [], 'series': []}}
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `M10` WHERE symbol = %s"
        cursor.execute(sql, symbol)
        result = cursor.fetchall()
        for r in result:
            res[symbol]['categories'].append(r['time'])
            serie = [r['open'], r['close'], r['low'], r['high']]
            res[symbol]['series'].append(serie)
    connection.commit()
    connection.close()
    return jsonify(res)

@quotations_blue_print.route('/web_get_rates_M10')
def web_get_rates_M10():
    res = {'EURUSD': [], 'USDJPY': [],'GBPUSD': [],'AUDUSD': [], 'USDCHF': [], 'USDCAD': []}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    for s in symbols_main:
        sql = "SELECT * FROM `M10` WHERE symbol = %s"
        cursor.execute(sql, s)
        result = cursor.fetchall()
        res[s] = result
    connection.commit()
    connection.close()
    return jsonify(res)


# 更新三个周期的行情
@quotations_blue_print.route('/update_rates')
def update_rates():
    res = {'status': 1}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    # 删除之前的数据
    sql1 = "DELETE FROM `D1`"
    cursor.execute(sql1)
    sql1 = "DELETE FROM `H1`"
    cursor.execute(sql1)
    sql1 = "DELETE FROM `M10`"
    cursor.execute(sql1)


    for s in symbols_main:
        rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_D1, 0, 60).tolist()

        for rate in rates:
            timeStamp = rate[0]
            dateArray = datetime.fromtimestamp(timeStamp)
            time = dateArray.strftime("%Y/%m/%d")
            sql2 = "INSERT INTO `D1` (`symbol`, `time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql2, (s, time, rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]))

        connection.commit()
        print(s, "D1   ok")

    for s in symbols_main:
        rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_H1, 0, 60).tolist()

        for rate in rates:
            timeStamp = rate[0]
            dateArray = datetime.fromtimestamp(timeStamp)
            time = dateArray.strftime("%Y/%m/%d  %H:%M:%S")
            sql2 = "INSERT INTO `H1` (`symbol`, `time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql2, (s, time, rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]))

        connection.commit()
        print(s, "H1   ok")


    for s in symbols_main:
        rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_M10, 0, 60).tolist()

        for rate in rates:
            timeStamp = rate[0]
            dateArray = datetime.fromtimestamp(timeStamp)
            time = dateArray.strftime("%Y/%m/%d  %H:%M:%S")
            sql2 = "INSERT INTO `M10` (`symbol`, `time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql2, (s, time, rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]))

        connection.commit()
        print(s, "M10   ok")

    # 更新时间
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql3 = "UPDATE `update_time` set `quotation` = %s"
    cursor.execute(sql3, now_time)
    connection.commit()


    connection.close()
    mt5.shutdown()
    return jsonify(res)