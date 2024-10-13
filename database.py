import mysql.connector

database = mysql.connector.connect(
    host=os.getenv('mysql.railway.internal'),
    user=os.getenv('root'),
    password=os.getenv('wXNZqAGgLJvHEngOmHHWqRkYmGiNliqw'),
    database=os.getenv('railway'),
    port=3306  # Puerto 3306 es por defecto
)
