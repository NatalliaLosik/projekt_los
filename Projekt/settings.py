from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_MYSQL_W = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': 'sakila'
}

DATABASE_MONGO_W = {
    'host': os.getenv('MONGO_HOST'),
    'user': os.getenv('MONGO_USER'),
    'authSource': os.getenv('MONGO_AUTH_SOURCE'),
    'password': os.getenv('MONGO_PASSWORD'),
    'db': os.getenv('MONGO_DB'),
    'args': "readPreference=primary&ssl=false&authMechanism=DEFAULT"
}