import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="erjgi58fl8iflu",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username.replace(' ', '') == '' or password.replace(' ', '') == '':
        records = [(0, 'Net znacheniya', '', '')]
    else:
        cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
        records = list(cursor.fetchall())
        if len(records) == 0:
            records = [(0, 'Net polzovatela', '', '')]
        else:
            records[0] = list(records[0])
            records[0][1] = 'Hello, ' + records[0][1]
            records[0][2] = 'login:' + records[0][2]
            records[0][3] = 'password:' + records[0][3]
    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
