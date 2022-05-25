import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully, DB add")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, dt_name):
    create_order_table = f"""
        CREATE TABLE IF NOT EXISTS {dt_name} (
        orders BIGINT NOT NULL UNIQUE,
        cost BIGINT NOT NULL,
        delivery_date TEXT,
        checks INTEGER)
        """
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(create_order_table)
        print("Query executed successfully, DT add")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, dt_name, order):
    select_orders = f"SELECT * FROM {dt_name} WHERE orders = {order}"
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(select_orders)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def create_record(connection, dt_name, orders, cost, delivery_date, now):
    insert_query = (
        f'INSERT INTO {dt_name} (orders, cost, delivery_date, checks) '
        f'VALUES {orders, cost, delivery_date, now}')
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(insert_query)


def execute_query_update(connection, dt_name, order, cost, delivery_date, now):
    update_order = F"""
    UPDATE
        {dt_name}
    SET
        cost = {cost}, delivery_date = '{delivery_date}', checks = {now}
    WHERE
        orders = {order}
    """
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(update_order)
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_read_query_order_check(connection, dt_name, now):
    select_check_orders = f'SELECT * FROM {dt_name} WHERE checks <> {now}'
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(select_check_orders)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def delete_order(connection, dt_name, now):
    delete_check_orders = f'DELETE FROM {dt_name} WHERE checks <> {now}'
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(delete_check_orders)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_read(connection, dt_name):
    select_orders = f"SELECT * FROM {dt_name}"
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(select_orders)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_read_query_today(connection, dt_name, today):
    select_orders = f"SELECT * FROM {dt_name} WHERE delivery_date = '{today}'"
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(select_orders)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")
