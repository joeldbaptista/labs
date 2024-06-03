import duckdb as db
import random as r
import logging
from faker import Faker
from datetime import datetime


ITEMS = ("Apple", "Rice", "Cheese")
DATABASE = "/app/data/database.db"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
	handlers=[
        logging.FileHandler("/var/log/cron_script.log"),
        logging.StreamHandler(),
    ]
)

def generate_event():
    """
    Generates an event
    """
    fake = Faker()
    name = fake.name()
    item = r.choice(ITEMS)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return ts, name, item


def insert_into_db(data):
    """
    Inserts `data` into database.purchases
    """
    try:
        with db.connect(DATABASE) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS purchases(
                    timestamp TIMESTAMP,
                    name TEXT,
                    item TEXT
                )
            """)
            conn.execute("INSERT INTO purchases VALUES (?, ?, ?)", data)
            logging.info(f"Inserted {data}")
    except Exception as err:
        logging.error(err)


if __name__ == "__main__":
    try:
        insert_into_db(generate_event())
    except Exception as err:
        logging.error(err)

