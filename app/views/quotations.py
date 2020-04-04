from flask import Blueprint, jsonify, request
from .. import config, logger, symbols_main
from datetime import datetime
import MetaTrader5 as mt5
import pymysql, time

quotations_blue_print = Blueprint('quotations_blue_print', __name__)

@quotations_blue_print.route('/update_rates_14')
def update_rates_14():
    res = {'status': 1}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    weekday = int(time.strftime("%w"))
    print(weekday)
    for s in symbols_main:
        rates = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_D1, 0, 14).tolist()
        if s == 'EURUSD':
            sql1 = "DELETE FROM `EURUSD_14`"
        if s == 'USDJPY':
            sql1 = "DELETE FROM `USDJPY_14`"
        if s == 'GBPUSD':
            sql1 = "DELETE FROM `GBPUSD_14`"
        if s == 'AUDUSD':
            sql1 = "DELETE FROM `AUDUSD_14`"
        if s == 'USDCHF':
            sql1 = "DELETE FROM `USDCHF_14`"
        if s == 'USDCAD':
            sql1 = "DELETE FROM `USDCAD_14`"
        cursor.execute(sql1)
        for rate in rates:
            timeStamp = rate[0]
            dateArray = datetime.fromtimestamp(timeStamp)
            time = dateArray.strftime("%Y/%m/%d")
            if s == 'EURUSD':
                 sql2 = "INSERT INTO `EURUSD_14` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            if s == 'USDJPY':
                sql2 = "INSERT INTO `USDJPY_14` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            if s == 'GBPUSD':
                sql2 = "INSERT INTO `GBPUSD_14` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            if s == 'AUDUSD':
                sql2 = "INSERT INTO `AUDUSD_14` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            if s == 'USDCHF':
                sql2 = "INSERT INTO `USDCHF_14` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            if s == 'USDCAD':
                sql2 = "INSERT INTO `USDCAD_14` (`time`, `open`, `high`, `low`, `close`, `tick_volume`, `spread`, `real_volume`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql2, (time, rate[1], rate[2], rate[3], rate[4], rate[5], rate[6], rate[7]))
        connection.commit()
    connection.close()
    mt5.shutdown()
    return jsonify(res)

@quotations_blue_print.route('/get_rates_14')
def get_rates_14():
    # Connect to the database
    connection = pymysql.connect(**config)
    res = {'EURUSD': {'categories': [], 'series': []}, 'USDJPY': {'categories': [], 'series': []}, 'GBPUSD': {'categories': [], 'series': []},
           'AUDUSD': {'categories': [], 'series': []}, 'USDCHF': {'categories': [], 'series': []}, 'USDCAD': {'categories': [], 'series': []}}
    with connection.cursor() as cursor:
        for s in symbols_main:
            if s == 'EURUSD':
                sql = "SELECT * FROM `EURUSD_14`"
            if s == 'USDJPY':
                sql = "SELECT * FROM `USDJPY_14`"
            if s == 'GBPUSD':
                sql = "SELECT * FROM `GBPUSD_14`"
            if s == 'AUDUSD':
                sql = "SELECT * FROM `AUDUSD_14`"
            if s == 'USDCHF':
                sql = "SELECT * FROM `USDCHF_14`"
            if s == 'USDCAD':
                sql = "SELECT * FROM `USDCAD_14`"
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                res[s]['categories'].append(r['time'])
                serie = [r['open'], r['high'], r['low'], r['close']]
                res[s]['series'].append(serie)
    connection.commit()
    connection.close()
    return jsonify(res)

@quotations_blue_print.route('/web_get_rates_14')
def web_get_rates_14():
    res = {'EURUSD': [], 'USDJPY': [],'GBPUSD': [],'AUDUSD': [], 'USDCHF': [], 'USDCAD': []}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    for s in symbols_main:
        if s == 'EURUSD':
            sql = "SELECT * FROM `EURUSD_14`"
        if s == 'USDJPY':
            sql = "SELECT * FROM `USDJPY_14`"
        if s == 'GBPUSD':
            sql = "SELECT * FROM `GBPUSD_14`"
        if s == 'AUDUSD':
            sql = "SELECT * FROM `AUDUSD_14`"
        if s == 'USDCHF':
            sql = "SELECT * FROM `USDCHF_14`"
        if s == 'USDCAD':
            sql = "SELECT * FROM `USDCAD_14`"
        cursor.execute(sql)
        result = cursor.fetchall()
        res[s] = result
    connection.commit()
    connection.close()
    return jsonify(res)
