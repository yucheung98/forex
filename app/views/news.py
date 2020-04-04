from flask import Blueprint, jsonify, request
from .. import config, logger
import pymysql, urllib.request, requests, urllib, re
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
    for i in range(6, 21):
        print(i)
        url = urllist[i].div.a.attrs['href']
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html)
        title = soup.section.h1.string
        news_from = soup.section.h3.a.string
        cover = urllist[i].div.img.attrs['src']
        comments_count = 0
        published_time = soup.section.h3.time.string
        content = str(soup.article.find_all('p')).split('[')[1].split(']')[0]

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
        content = str(soup.article.find_all('p')).split('[')[1].split(']')[0]

        sql = "INSERT INTO `news_focus` (`title`, `news_from`, `cover`, `comments_count`, `published_time`, `content`) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (title, news_from, cover, comments_count, published_time, content))
        print('news_focus----ok!')

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




