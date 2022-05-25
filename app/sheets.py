import os
import time
from datetime import datetime

import apiclient
import db_func
import exchange
import httplib2
import psycopg2
import telegram
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

CREDENTIALS_FILE = 'creds.json'
SHEET_ID = '1TLzoKENjVoH7SqWL2EDENxq63FMY94ugxcQqnRx30nc'
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
DB_NAME = os.getenv('DB_NAME')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

"""
Время между итерациями проверки google sheets.
"""
RETRY_TIME = 60

usd = exchange.exchange()

"""
Название для создаваемой таблицы.
"""
dt_name = 'order21121'


def google_sheets_api(var1, var2):
    """
    Получаем API документа.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']
         )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    values = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range='A2:E',
        majorDimension='ROWS'
    ).execute()
    return values['values']


def send_message(bot, message):
    """
    Отправляем сообщение о наступлении дня исполнения обязательств.
    """
    try:
        bot.send_message(TELEGRAM_CHAT_ID, text=message)
    except telegram.TelegramError:
        print('Сбой при отправке сообщения')


if __name__ == "__main__":
    while True:
        connection = db_func.create_connection(
            DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT)
        db_func.execute_query(connection, dt_name)
        now = int(datetime.now().strftime("%M"))
        today = datetime.now().strftime('%d.%m.%Y')
        result = google_sheets_api(CREDENTIALS_FILE, SHEET_ID)
        for order in result:
            order[1] = int(order[1])
            cost = int(int(order[2]) * usd)
            if db_func.execute_read_query(connection, dt_name, order[1]) == []:
                db_func.create_record(connection, dt_name, order[1], cost,
                                      order[3], now)
            else:
                db_func.execute_query_update(connection, dt_name, order[1],
                                             cost, order[3], now)
        if len(db_func.execute_read_query_order_check(connection,  dt_name,
                                                      now)) != 0:
            try:
                db_func.delete_order(connection, dt_name, now)
            except psycopg2.ProgrammingError:
                pass
        find_orders_today = db_func.execute_read_query_today(connection,
                                                             dt_name, today)
        if len(find_orders_today) != 0:
            orders_list = []
            orders_list = ', '.join([str(day[0]) for day in find_orders_today])
            bot = telegram.Bot(TELEGRAM_TOKEN)
            send_message(bot,
                         message=f'По заказам {orders_list}'
                         ' наступил день исполнения!')
        time.sleep(RETRY_TIME)
