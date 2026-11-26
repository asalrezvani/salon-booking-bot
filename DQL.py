import mysql.connector
from config import *


def get_known_user():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM CUSTOMER;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return {row['CID']: row for row in data}

def get_customer_data():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM CUSTOMER;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def get_personnel_data(ID):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM PERSONNEL WHERE ID=%s;",(ID,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def get_personnel_id(name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT ID FROM PERSONNEL WHERE NAME=%s;",(name,))
    personnel_id = cur.fetchone()
    cur.close()
    conn.close()
    return personnel_id['ID']

def get_category_data():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT NAME FROM CATEGORY;")
    category_info = cur.fetchall()
    cur.close()
    conn.close()
    return category_info

def get_category_id(name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT ID FROM CATEGORY WHERE NAME=%s;',(name,))
    category_id = cur.fetchone()
    cur.close()
    conn.close()
    return category_id["ID"]


def get_service_data(categ_id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT NAME FROM SERVICE WHERE CATEG_ID=%s;",(categ_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_service_id(name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT ID FROM SERVICE WHERE NAME=%s;",(name,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data['ID']

def get_service_duration(ID):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT DURATION FROM SERVICE WHERE ID=%s;",(ID,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data['DURATION']

def get_personnel_service_data(pers_id,serv_id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT ID FROM PERSONNEL_SERVICE WHERE PERS_ID=%s AND SERV_ID=%s;",(pers_id,serv_id))
    data = cur.fetchone()
    cur.close()
    conn.close()    
    return data['ID']

def get_personnel_service_id(serv_id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT PERS_ID FROM PERSONNEL_SERVICE WHERE SERV_ID=%s;",(serv_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [row ['PERS_ID'] for row in data]

def get_taking_turn_data():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM TAKING_TURN;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_taking_turn_date(cust_id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT DATE,STATUS FROM TAKING_TURN WHERE CUST_ID=%s;",(cust_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return {row['DATE'] : row['STATUS'] for row in data}

def get_capacity_data(ID):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM CAPACITY WHERE ID=%s;",(ID,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data


if __name__ == '__main__':
    pass

