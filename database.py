import os
import mysql.connector

database = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'autorack.proxy.rlwy.net'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASS', 'wXNZqAGgLJvHEngOmHHWqRkYmGiNliqw'),
    database=os.getenv('DB_NAME', 'railway'),
    port=os.getenv('DB_PORT', 56559)
)
