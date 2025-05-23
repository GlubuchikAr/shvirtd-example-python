import json

from flask import Flask
from flask import request
import os
import mysql.connector
from datetime import datetime

app = Flask(__name__)
db_host=os.environ.get('DB_HOST')
db_user=os.environ.get('DB_USER')
db_password=os.environ.get('DB_PASSWORD')
db_database=os.environ.get('DB_NAME')

# Подключение к базе данных MySQL
db = mysql.connector.connect(
host=db_host,
user=db_user,
password=db_password,
database=db_database,
autocommit=True )
cursor = db.cursor()

# SQL-запрос для создания таблицы в БД
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {db_database}.requests (
id INT AUTO_INCREMENT PRIMARY KEY,
request_date DATETIME,
request_ip VARCHAR(255),
request_data TEXT
)
"""
cursor.execute(create_table_query)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Получение IP-адреса пользователя
    ip_address = request.headers.get('X-Forwarded-For')
    data = request.data.decode('utf-8')
 #   try:
 #       data = json.loads(request.data.decode('utf-8'))
 #   except json.JSONDecodeError:
 #       data = ""

    # Запись в базу данных
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    query = "INSERT INTO requests (request_date, request_ip, request_data) VALUES (%s, %s, %s)"
    values = (current_time, ip_address, data)
    cursor.execute(query, values)
    db.commit()

    return f'TIME: {current_time}, IP: {ip_address}, BODY: {data}'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
