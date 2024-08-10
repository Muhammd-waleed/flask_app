from flask import Flask
import pymysql as mq

connection=mq.connect(host='localhost', 
                     user='root',
                     password='',
                     port=3306, 
                     database='flask_app_mysql_db',
                     cursorclass=mq.cursors.DictCursor)

app=Flask(__name__)
app.config['SECRET_KEY']='2463ed925ee56413c77f5282'

from market import routes