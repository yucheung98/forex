from flask import Blueprint, jsonify, request
from .. import config, logger
import pymysql, urllib.request, requests, urllib, re, datetime
from bs4 import BeautifulSoup

news_blue_print = Blueprint('news_blue_print', __name__)

@news_blue_print.route('/update_news')
def update_news():
    res = {'status': 1}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()

    url = 'http://www.cnforex.com/'
    html = urllib.request.urlopen(url).read()
    soup_ = BeautifulSoup(html)

    sql1 = "DELETE FROM `news`"
    cursor.execute(sql1)
    urllist = soup_.find_all('figure')
    print(len(urllist))
    for i in range(7, 22):
        print(i)
        url = urllist[i].div.a.attrs['href']
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html)
        title = soup.section.h1.string
        news_from = soup.section.h3.a.string
        cover = urllist[i].div.img.attrs['src']
        comments_count = 0
        published_time = soup.section.h3.time.string
        content = soup.article.find_all('p')
        for j in range(len(content)):
            content[j] = str(content[j])
        content = "".join(content)

        sql = "INSERT INTO `news` (`title`, `news_from`, `cover`, `comments_count`, `published_time`, `content`) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (title, news_from, cover, comments_count, published_time, content))

    sql2 = "DELETE FROM `news_focus`"
    cursor.execute(sql2)
    urlfocuslist = soup_.find_all('figure',class_= re.compile(r"^normal"))
    for u in urlfocuslist:
        url = u.a.attrs['href']
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html)
        title = soup.section.h1.string
        news_from = soup.section.h3.a.string
        cover = u.img.attrs['src']
        comments_count = 0
        published_time = soup.section.h3.time.string
        content = soup.article.find_all('p')
        for j in range(len(content)):
            content[j] = str(content[j])
        content = "".join(content)

        sql = "INSERT INTO `news_focus` (`title`, `news_from`, `cover`, `comments_count`, `published_time`, `content`) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (title, news_from, cover, comments_count, published_time, content))
        print('news_focus----ok!')
    # 清空评论表
    sql3 = "DELETE FROM `news_comments`"
    cursor.execute(sql3)
    # 更新时间
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql4 = "UPDATE `update_time` set `news` = %s"
    cursor.execute(sql4, now_time)
    connection.commit()
    connection.close()
    return jsonify(res)

@news_blue_print.route('/get_news')
def get_news():
    res = []
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()

    sql = "SELECT * FROM `news`"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    result = cursor.fetchall()
    for r in result:
        res.append(r)
    return jsonify(res)

@news_blue_print.route('/get_news_focus')
def get_news_focus():
    res = []
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()

    sql = "SELECT * FROM `news_focus`"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    result = cursor.fetchall()
    for r in result:
        res.append(r)
    return jsonify(res)

@news_blue_print.route('/get_news_comments', methods=['POST'])
def get_news_comments():
    req = request.json
    logger.info(req)
    news_id = req['news_id']
    res = []
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()

    sql = "SELECT * FROM `news_comments` WHERE `news_id` = %s"
    cursor.execute(sql, news_id)
    connection.commit()
    connection.close()
    result = cursor.fetchall()
    for r in result:
        res.append(r)
    return jsonify(res)

@news_blue_print.route('/get_update_time')
def get_news_update_time():
    res = {}
    # Connect to the database
    connection = pymysql.connect(**config)
    cursor = connection.cursor()

    sql = "SELECT * FROM `update_time` WHERE `id` = 1"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    result = cursor.fetchall()[0]
    res = result
    return jsonify(res)

@news_blue_print.route('/delete_news_comment', methods=['POST'])
def delete_news_comment():
    req = request.json
    id = req['id']
    res = {}
    res1 = {'status': 1}
    res2 = {'status': 0}
    # Connect to the database
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM news_comments WHERE id = %s"
            cursor.execute(sql, id)
            sql2 = "SELECT * FROM `news_comments` WHERE news_id = %s"
            cursor.execute(sql2, news_id)
            comments_count = len(cursor.fetchall())
            sql3 = "UPDATE `news` SET comments_count = %s  WHERE news_id = %s"
            cursor.execute(sql3, (comments_count, news_id))
            sql4 = "UPDATE `news_focus` SET comments_count = %s  WHERE news_id = %s"
            cursor.execute(sql4, (comments_count, news_id))
            res = res1
        connection.commit()
    finally:
        logger.info(res)
        connection.close()
    return jsonify(res)

@news_blue_print.route('/insert_news_comment', methods=['POST'])
def insert_news_comment():
    req = request.json
    news_id = req['news_id']
    user_name = req['user_name']
    comment = req['comment']
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res = {}
    # Connect to the database
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `news_comments` (`news_id`, `user_name`, `time`, `comment` ) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (news_id, user_name, now_time, comment))
            sql2 = "SELECT * FROM `news_comments` WHERE news_id = %s"
            cursor.execute(sql2, news_id)
            comments_count = len(cursor.fetchall())
            sql3 = "UPDATE `news` SET comments_count = %s  WHERE news_id = %s"
            cursor.execute(sql3, (comments_count, news_id))
            sql4 = "UPDATE `news_focus` SET comments_count = %s  WHERE news_id = %s"
            cursor.execute(sql4, (comments_count, news_id))
            res = {'status': 1}
        connection.commit()
    finally:
        logger.info(res)
        connection.close()
    return jsonify(res)