import json
import pymysql
import mysql.connector
import pymysql.cursors
from fastapi import HTTPException


class Db:
    def __init__(self):
        pass

    # This class method read the mysql connection information from my password file.
    # and creates a connection.
    @classmethod
    def connect(cls):
        connection_vault_path = '/Users/user/pwd.json'

        try:
            with open(connection_vault_path, 'r') as connection_file:
                connection_dict = json.load(connection_file)
            return pymysql.connect(
                host=connection_dict['host'],
                user=connection_dict['user'],
                password=connection_dict['password'],
                database=connection_dict['database'],
                cursorclass=pymysql.cursors.DictCursor
            )
        except FileNotFoundError:
            print(f"File '{connection_vault_path}' not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")


class SqlData(Db):

    def __init__(self):
        super().__init__()

    # execute any multi-rol query and return the results.
    @staticmethod
    def sql(s):
        conn = Db.connect()
        cursor = conn.cursor()
        cursor.execute(s)
        records = cursor.fetchall()
        return records

    # execute any single row query and return the results.
    @staticmethod
    def sql0(s):
        conn = Db.connect()
        cursor = conn.cursor()
        cursor.execute(s)
        records = cursor.fetchone()
        return records

    # execute any SQL command that changes data.
    @staticmethod
    def execute(s):
        conn = Db.connect()
        cursor = conn.cursor()
        cursor.execute(s)
        conn.commit()
        return

    # post data to a table.
    # -- id: primary key of the table.
    # -- table_name: the name of the table.
    # -- action: "insert" or "delete".
    # The naming convention includes an autonumber primary key called 'id'
    # and a date column called 'create_timestamp'.

    @staticmethod
    def post(my_dict):

        # if 'id' is not in the dictionary, it is automatically an INSERT.
        if 'id' not in my_dict:
            my_id = 0
        else:
            my_id = my_dict['id']

        # if 'action' is not in the dictionary, it is automatically an INSERT.
        if 'action' not in my_dict:
            my_action = "insert"
        else:
            my_action = my_dict['action']

        # if 'table_name' is not in the dictionary, throw an error.
        if 'table_name' not in my_dict:
            return 900
        else:
            table_name = my_dict['table_name']

        # connect to the database.
        conn = Db.connect()
        # create a cursor.
        cursor = conn.cursor()
        # insert or update
        if my_action == 'insert' or my_action == 'update':
            # insert a new record if the id passed is 0 or doesn't exit.
            if my_id == 0 or my_id == '':
                sql = "insert into " + table_name + "(create_timestamp) values (now())"
                cursor.execute(sql)
                conn.commit()

                cursor.execute("SELECT LAST_INSERT_ID() AS C")
                records = cursor.fetchall()
                my_id = records[0]['C']

            # iterate through each column in the dict.
            for key in my_dict:
                # update the column in the table if it is not a reserved word or 'id' or 'create_timestamp';
                if key != 'table_name' and key != 'id' and key != 'create_timestamp' and key != 'action':
                    cursor = conn.cursor()
                    sql = "update " + table_name + " set " + key + " = %s where id = %s"
                    v = (my_dict[key], my_id)
                    cursor.execute(sql, v)
            conn.commit()
        # delete
        if my_action == 'delete':
            sql = "delete from " + table_name + " where id = " + my_id
            cursor.execute(sql)

        return my_id
