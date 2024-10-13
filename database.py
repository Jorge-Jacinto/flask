import os
import mysql.connector

database = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'mysql.railway.internal'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASS', 'wXNZqAGgLJvHEngOmHHWqRkYmGiNliqw'),
    database=os.getenv('DB_NAME', 'railway'),
    port=os.getenv('DB_PORT', 3306)
)
