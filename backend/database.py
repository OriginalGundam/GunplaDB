#Connects to PostgreSQL

import psycopg2
from config import *

def get_connection():

    connection = psycopg2.connect(

        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT

    )

    return connection