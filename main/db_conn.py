# sudo python3 -m pip install mysql-connector-python
# pip3 install python-dotenv
import mysql.connector
from dotenv import load_dotenv
from os.path import getsize
from os.path import exists
import os

class DBConn():
    # Config variables
    ACCESS_TOKEN = "ACCESS_TOKEN"
    CURR_GAME = "CURR_GAME"

    # Light config variables
    CURR_MAT = "CURR_MATRIX"
    CURR_STRIP = "CURR_STRIP"
    DEF_MAT = "DEFAULT_MATRIX"
    DEF_STRIP = "DEFAULT_STRIP"

    def __init__(self):
        if not exists(".env"):
            raise Exception(".env file not found")
        
        load_dotenv()

    def connect(self):
        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )
        if self.mydb.is_connected():
            self.cursor = self.mydb.cursor()

    def disconnect(self):
        if self.mydb.is_connected():
            self.cursor.close()
            self.mydb.close()
    
    def query(self, query):
        if not self.mydb.is_connected():
            return ""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute(self, query):
        if not self.mydb.is_connected():
            return ""
        self.cursor.execute(query)
        self.mydb.commit()

    def get_evar(self, evar):
        # [(EVAR, VAL)]
        res = self.query(f"SELECT * FROM CONFIG WHERE evar = '{evar}'")
        return res[0][1] if len(res) else ""

    def set_evar(self, evar, val):
        self.execute(f"DELETE FROM CONFIG WHERE evar = '{evar}'")
        if self.get_evar(evar) == "":
            self.execute(f"INSERT INTO CONFIG (evar, val) VALUES ('{evar}', '{val}')")

    def reset_config(self):
        self.set_evar(self.CURR_MAT, "")
        self.set_evar(self.CURR_STRIP, "")
        self.set_evar(self.DEF_MAT, "jj.png")
        self.set_evar(self.DEF_STRIP, "255,0,0")
