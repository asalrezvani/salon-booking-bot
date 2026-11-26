import mysql.connector
from config import *
from texts import *

def drop_n_create_database(db_name):
    conn = mysql.connector.connect(user = db_config['user'] , password = db_config['password'] , host = db_config['host'])
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
    cur.close()
    conn.close()

    print(f'database {db_name} created successfully.')


def create_table_customer():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE CUSTOMER(
                `CID`            BIGINT UNSIGNED NOT NULL PRIMARY KEY,
                `NAME`           VARCHAR(50) NOT NULL,
                `PHONE`          VARCHAR(13) UNIQUE NOT NULL,
                `BIRTH_DATE`     DATE,
                `REGISTER_DATE`  DATETIME DEFAULT CURRENT_TIMESTAMP,
                `LAST_UPDATE`    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """)
    cur.close()
    conn.close()
    print('table customer created successfully.')


def create_table_personnel():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE PERSONNEL(
                `ID`             INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `NAME`           VARCHAR(20) NOT NULL,
                `REGISTER_DATE`  DATETIME DEFAULT CURRENT_TIMESTAMP,
                `LAST_UPDATE`    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """)
    cur.close()
    conn.close()
    print('table personnel created successfully.')


def create_table_category():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE CATEGORY(
                `ID`             INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `NAME`           VARCHAR(50) NOT NULL,
                `REGISTER_DATE`  DATETIME DEFAULT CURRENT_TIMESTAMP,
                `LAST_UPDATE`    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """)
    cur.close()
    conn.close()
    print('table category created successfully.')


def create_table_service():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE SERVICE(
                `ID`             INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `CATEG_ID`       INT UNSIGNED NOT NULL, 
                `NAME`           VARCHAR(50) NOT NULL,
                `DURATION`       TIME,
                `REGISTER_DATE`  DATETIME DEFAULT CURRENT_TIMESTAMP,
                `LAST_UPDATE`    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (CATEG_ID) REFERENCES CATEGORY(ID)
                );
                """)
    cur.close()
    conn.close()
    print('table service created successfully.')


def create_table_personnel_service():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE PERSONNEL_SERVICE(
                `ID`             INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `PERS_ID`        INT UNSIGNED NOT NULL,
                `SERV_ID`        INT UNSIGNED NOT NULL,
                `REGISTER_DATE`  DATETIME DEFAULT CURRENT_TIMESTAMP,
                `LAST_UPDATE`    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (PERS_ID) REFERENCES PERSONNEL(ID),
                FOREIGN KEY (SERV_ID) REFERENCES SERVICE(ID),
                UNIQUE (PERS_ID , SERV_ID)
                );
                """)
    cur.close()
    conn.close()
    print('table personnel_service created successfully.')


def create_table_taking_turn():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE TAKING_TURN(
                `ID`             INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `CUST_ID`        BIGINT UNSIGNED NOT NULL,
                `PERS_SERV_ID`   INT UNSIGNED NOT NULL,
                `DATE`           DATE NOT NULL,
                `TIME`           TIME NOT NULL,
                `STATUS`         VARCHAR(20) NOT NULL,
                `REGISTER_DATE`  DATETIME DEFAULT CURRENT_TIMESTAMP,
                `LAST_UPDATE`    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (CUST_ID) REFERENCES CUSTOMER(CID),
                FOREIGN KEY (PERS_SERV_ID) REFERENCES PERSONNEL_SERVICE(ID)
                );
                """)
    cur.close()
    conn.close()
    print('table taking_turn created successfully.')


def create_table_capacity():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE CAPACITY(
                `ID`             INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `PERS_SERV_ID`   INT UNSIGNED NOT NULL,
                `DATE`           DATE NOT NULL,
                `MAX_CAPACITY`   INT UNSIGNED NOT NULL,
                `REGISTER_DATE`  DATETIME DEFAULT CURRENT_TIMESTAMP,
                `LAST_UPDATE`    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (PERS_SERV_ID) REFERENCES PERSONNEL_SERVICE(ID)
                );
                """)
    cur.close()
    conn.close()
    print('table capacity created successfully.')

def insert_personnel_data(name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute('INSERT INTO PERSONNEL (NAME) VALUES (%s);',(name,))
    conn.commit()
    cur.close()
    conn.close()
    print('personnel data inserted successfully.')

def insert_category_data(name):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute('INSERT INTO CATEGORY (NAME) VALUES (%s);',(name,))
    conn.commit()
    cur.close()
    conn.close()
    print('catagory data inserted successfully.')

def insert_service_data(categ_id,name,duration):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute('INSERT INTO SERVICE (CATEG_ID,NAME,DURATION) VALUES (%s,%s,%s);',(categ_id,name,duration))
    conn.commit()
    cur.close()
    conn.close()
    print('service data inserted successfully.')

def insert_personnel_service_data(pers_id,serv_id):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor(dictionary=True)
    cur.execute('INSERT INTO PERSONNEL_SERVICE (PERS_ID,SERV_ID) VALUES (%s,%s);',(pers_id,serv_id))
    conn.commit()
    cur.close()
    conn.close()
    print('personnel_service inserted successfully.')

if __name__ == '__main__':
    drop_n_create_database(db_name= db_config['database'])
    create_table_customer()
    create_table_personnel()
    create_table_category()
    create_table_service()
    create_table_personnel_service()
    create_table_taking_turn()
    create_table_capacity()
    insert_personnel_data(text['sara'])
    insert_personnel_data(text['mahsa'])
    insert_personnel_data(text['mina'])
    insert_personnel_data(text['zahra'])
    insert_personnel_data(text['pari'])
    insert_personnel_data(text['tina'])
    insert_personnel_data(text['aisan'])    
    insert_personnel_data(text['marjan'])
    insert_personnel_data(text['zohre'])
    insert_personnel_data(text['nastaran'])
    insert_personnel_data(text['nasrin'])
    insert_personnel_data(text['maryam'])
    insert_category_data(text['hair'])
    insert_category_data(text['nail'])
    insert_category_data(text['eyelash'])
    insert_service_data(1, text['color_hair'], '02:00:00')
    insert_service_data(1, text['baft_hair'], '00:30:00')
    insert_service_data(1, text['cut_hair'], '00:30:00')
    insert_service_data(1, text['extention_hair'], '03:00:00')
    insert_service_data(1, text['keratin_hair'], '4:00:00')
    insert_service_data(2, text['kasht_nail'], '02:00:00')
    insert_service_data(2, text['tarmim_nail'], '01:30:00')
    insert_service_data(2, text['tarmim_pa_nail'], '00:40:00')
    insert_service_data(2, text['pedikur_nail'], '01:00:00')
    insert_service_data(3, text['kasht_eyelash'], '00:40:00')
    insert_service_data(3, text['extention_eyelash'], '02:00:00')
    insert_personnel_service_data(1,1)
    insert_personnel_service_data(1,5)
    insert_personnel_service_data(2,1)
    insert_personnel_service_data(2,3)
    insert_personnel_service_data(3,2)
    insert_personnel_service_data(4,4)
    insert_personnel_service_data(5,4)
    insert_personnel_service_data(5,5)
    insert_personnel_service_data(6,5)
    insert_personnel_service_data(7,6)
    insert_personnel_service_data(7,7)
    insert_personnel_service_data(8,6)
    insert_personnel_service_data(8,7)
    insert_personnel_service_data(9,8)
    insert_personnel_service_data(9,9)
    insert_personnel_service_data(10,10)
    insert_personnel_service_data(11,10)
    insert_personnel_service_data(12,11)
