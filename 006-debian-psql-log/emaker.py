"""
Event maker
"""
import os
import time
import logging
import random
import psycopg2 as pg

from prometheus_client import start_http_server, Info
from messages import messages


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%y-%m-%d %H:%M:%S', level=logging.INFO,
)

INFO_METRIC = Info("send_message", "The message sent to the database")
PROMETHEUS_PORT = 8000
CREDENTIALS = {
    "host": "db",
    "port": 5432, 
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DB"),
}


def send_data_to_db(run_id, message):
    logging.info(f"Inserting {run_id}: {message}")
    with pg.connect(**CREDENTIALS) as con:
        cur = con.cursor()
        cur.execute(f"""
            INSERT INTO aaa.events(run_id, message) VALUES (%s, %s)
        """, (run_id, message))
        con.commit()


def wait_for_ready():
    is_ready = False
    logging.info("Checking if the DB is ready")
    time.sleep(5)
    with pg.connect(**CREDENTIALS) as con:
        cur = con.cursor()
        while not is_ready:
            logging.info("Check if DB is ready")
            cur.execute("SELECT status FROM aaa.status");
            res = cur.fetchone()
            is_ready = res[0] == 'ready'
            if not is_ready:
                logging.info("DB not ready yet!")
                time.sleep(5)
    logging.info("DB is ready to receive data")



if __name__ == "__main__":
    run_id = 1
    wait_for_ready()
    start_http_server(PROMETHEUS_PORT)
    while True:
        message = random.choice(messages)
        send_data_to_db(run_id=run_id, message=message)
        INFO_METRIC.info({"run_id": str(run_id), "message": message})
        run_id += 1
        time.sleep(5)

