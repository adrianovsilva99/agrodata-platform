import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def check_database_connection():
    connection = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

            if result == (1,):
                print("Database connection successful.")
            else:
                print("Unexpected database response.")

    finally:
        connection.close()


if __name__ == "__main__":
    check_database_connection()