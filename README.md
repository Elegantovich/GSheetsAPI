# GSheetsAPI

### Tech
Python 3.7, Docker, PostgreSQL, Google API.

## Описание.

Скрипт **GSheetsAPI** получает по API актуальные данные из google sheets. Данные могут обновляться, добавляться и удаляться. Данные сохраняются в БД PostgreSQL. При наступлении срока исполнения обязательств по заказу на ваш телеграмм придет соответсвующее уведомление. 

## Установка на локальном компьютере.
Эти инструкции помогут вам создать копию проекта и запустить ее на локальном компьютере для целей разработки и тестирования.

### Установка Docker.
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск проекта.
Склонируйте этот репозиторий в текущую папку
```
git clone https://github.com/elegantovich/GSheetsAPI/
```
Создайте файл `.env` командой
```
touch .env
```
и добавьте в него переменные окружения для работы с базой данных:
```
TELEGRAM_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432 
```
Запустите docker-compose:
```
docker-compose up -d --build
```

### Важно знать:
- период между итерациями == 60сек. Настраивается опционально в app/sheets.py.
- документ с учетными данными должен быть сохранен в директории app/ и носить имя `creds.json`.

ссылка на [документ](https://docs.google.com/spreadsheets/d/1TLzoKENjVoH7SqWL2EDENxq63FMY94ugxcQqnRx30nc/edit?usp=sharing)
### Авторы:

[Хачатрян Максим](https://github.com/Elegantovich)<br>
