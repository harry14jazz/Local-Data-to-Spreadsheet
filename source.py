import mysql.connector
from decouple import config

def connect_to_mysql():

    try:
        mydb = mysql.connector.connect(
            host=config('host'),
            user=config('user'),
            password=config('password'),
            database=config('database')
        )

    except mysql.connector.Error as err:
        print(err)
        print("Message ", err.msg)

    return mydb

def get_db_cursor(db_conn):
    try:
        mycursor = db_conn.cursor()
    
    except mysql.connector.Error as err:
        print(err)
        print("Message ", err.msg)

    return mycursor 

# connecting = connect_to_mysql()
# res = get_db_cursor(connecting)
# print(res)