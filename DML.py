import mysql.connector
from config import *


def insert_customer_data(cid,name,phone,birth_date=None):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO CUSTOMER (CID,NAME,PHONE,BIRTH_DATE) VALUES (%s,%s,%s,%s);", (cid,name,phone,birth_date))
    conn.commit()
    customer_data = cur.lastrowid
    cur.close()
    conn.close()
    return customer_data

def insert_personnel_data(name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO PERSONNEL (NAME) VALUE (%s);" , (name,))
    conn.commit()
    personnel_id = cur.lastrowid
    cur.close()
    conn.close()
    return personnel_id


def insert_category_data(name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO CATEGORY (NAME) VALUES (%s);" , (name,))
    conn.commit()
    category_id = cur.lastrowid
    cur.close()
    conn.close()
    return category_id

def insert_service_data(categ_id,name,duration=None):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO SERVICE (CATEG_ID,NAME,DURATION) VALUES (%s,%s,%s);" , (categ_id,name,duration))
    conn.commit()
    service_id = cur.lastrowid
    cur.close()
    conn.close()
    return service_id

def insert_personnel_service_data(pers_id,serv_id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO PERSONNEL_SERVICE (PERS_ID,SERV_ID) VALUES (%s,%s);" , (pers_id,serv_id))
    conn.commit()
    data = cur.lastrowid
    cur.close()
    conn.close()
    return data


def insert_taking_turn_data(cust_id,pers_serv_id,date,time,status):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO TAKING_TURN (CUST_ID,PERS_SERV_ID,DATE,TIME,STATUS) VALUES (%s,%s,%s,%s,%s);" , (cust_id,pers_serv_id,date,time,status))
    conn.commit()
    data = cur.lastrowid
    cur.close()
    conn.close()
    return data

def update_taking_turn_status(CUST_ID):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute("UPDATE TAKING_TURN SET STATUS = 'cancel' WHERE CUST_ID=%s;",(CUST_ID,))
    conn.commit()
    cur.close()
    conn.close()


def insert_capacity_data(pers_serv_id,date,max_capacity):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO CAPACITY (PERS_SERV_ID,DATE,MAX_CAPACITY) VALUES (%s,%s,%s);" , (pers_serv_id,date,max_capacity))
    capacity_id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return capacity_id

if __name__ == '__main__':
    pass
