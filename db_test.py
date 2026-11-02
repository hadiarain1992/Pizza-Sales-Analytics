from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = "root"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_NAME = "pizza_sales"

connection_url = URL.create(
    "mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME
)

try:
    engine = create_engine(connection_url)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE()"))
        print("CONNECTED SUCCESSFULLY!")
        print("Database:", result.scalar())
except Exception as error:
    print("CONNECTION FAILED:")
    print(error)