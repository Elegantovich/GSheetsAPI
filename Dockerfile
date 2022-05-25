FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app
COPY ./app /app

RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir

WORKDIR /app

CMD ["python3", "sheets.py"] 