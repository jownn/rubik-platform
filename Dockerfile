FROM python:3.6

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN python create_db.py

EXPOSE 5000