import mysql.connector
from config import *

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
if __name__ == '__main__':
    pass
