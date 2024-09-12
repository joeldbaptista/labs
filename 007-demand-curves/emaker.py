"""
Event maker
"""
import json
import logging
import random
import argparse
import datetime as dt
import psycopg2 as pg

from typing import Tuple, List, Dict


logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%y-%m-%d %H:%M:%S", 
    level=logging.INFO,
)


def validate_date(date_str: str) -> dt.datetime:
    try:
        return dt.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as err:
        error(err)


def get_argsparser() -> argparse.ArgumentParser:
    """
    Returns the CLI arguments

    Returns:
        argparse.ArgumentParser object
    """
    parser = argparse.ArgumentParser(
        description="Generates events according to a demand curve"
    )
    parser.add_argument(
        "--config", type=str, required=True, help="The mandatory configuration YAML file"
    )
    parser.add_argument(
        "--start", type=validate_date, required=True, help="The start datetime"
    )
    parser.add_argument(
        "--end", type=validate_date, required=True, help="The end datetime"
    )
    return parser


def validate_args(parser: argparse.ArgumentParser) -> Tuple:
    """
    Validates the arguments
    """
    args = parser.parse_args()
    config = args.config
    start = args.start
    end = args.end
    return config, start, end


def error(msg: str, exit_code: int=1):
    """
    Logs an error with message `msg`, and exits the script with code `exit_code`
    """
    logging.error(msg)
    exit(exit_code)


def info(msg: str):
    """
    Logs an info with message `msg`
    """
    logging.info(msg)


def read_json(fname: str) -> List|Dict:
    try:
        with open(fname, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as err:
        error(str(err))
    except Exception as err:
        error(str(err))


def random_timestamps(t0: dt.datetime, t1: dt.datetime, n: int) -> List[dt.datetime]:
    if t0 < t1:
        total_seconds = (t1 - t0).total_seconds()
        nn = random.randint(0, n) # Randomly pick a number of occurences
        return [
            t0 + dt.timedelta(seconds=random.uniform(0, total_seconds))
            for _ in range(nn)
        ]
    raise ValueError("random_timstamps: t0 >= t1")


CREDENTIALS = {
    "host": "localhost",
    "port": 5432, 
    "user": "postgres",
    "password": "1234",
    "dbname": "sandbox",
}


def send_data_to_db(insert_query: str):
    logging.info("Inserting events")
    with pg.connect(**CREDENTIALS) as con:
        cur = con.cursor()
        cur.execute(insert_query)
        con.commit()


if __name__ == "__main__":
    parser = get_argsparser()
    config, start, end = validate_args(parser)
    demand_curve = sorted(
        (
            (
                dt.datetime.strptime(
                    r["t0"] if r["t0"] != "24:00:00" else "23:59:59", "%H:%M:%S",
                ),
                dt.datetime.strptime(
                    r["t1"] if r["t1"] != "24:00:00" else "23:59:59", "%H:%M:%S",
                ), 
                r["nevents"],
            ) for r in read_json(config)
        ), key=lambda r: r[0],
    )
    # Create events
    values = []
    while start < end:
        for t0, t1, ne in demand_curve: 
            dt0 = dt.datetime.combine(start.date(), t0.time())
            dt1 = dt.datetime.combine(start.date(), t1.time())
            values.extend(
                f"('{e}')" for e in random_timestamps(dt0, dt1, ne)
            )
        start += dt.timedelta(days=1)
    # Compose the insert query
    insert_query = f"""
        INSERT INTO events.pizzaria_occurences(request_ts) 
        VALUES {', '.join(values)}
    """
    send_data_to_db(insert_query)


