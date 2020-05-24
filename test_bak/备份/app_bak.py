import logging
import pymysql.cursors
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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



@app.route('/login', methods=['POST'])
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)