import requests


def exchange():
    r = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    r = r.text.split('Доллар США')
    r = r[1].split('<')
    r = r[2].split('Value>')
    exchange_rate = float(r[1].replace(',', '.'))
    return exchange_rate
