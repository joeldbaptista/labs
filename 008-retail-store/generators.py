"""
Implements a generator
"""
import random

from faker import Faker
from typing import List
from typing import List, Dict
from functools import cmp_to_key
from datetime import datetime, timedelta


ADJECTIVES = [
    'Durable', 
    'Comfortable', 
    'Portable', 
    'Stylish', 
    'Affordable', 
    'Compact', 
    'Versatile', 
    'Reliable', 
    'Elegant', 
    'Lightweight',
]

def _calculate_execution_thread_(entities: List[str]):
    """
    Calculates the dependencies between the different entities
    """
    # TODO validate if names being use in FK exist; guard from typos
    deps = { e:[] for e in entities }
    ents = [ e    for e in entities ]

    # Set ancestors
    for e in entities:
        schema = entities[e]["schema"]
        for s in schema:
            v = schema[s]
            if v["use"] == "generate_foreign_key":
                args = v["args"]
                deps[e].append(args["entity"])

    # Sort entities    
    return sorted(
        ents, key=cmp_to_key(lambda e1, e2: e1 in deps[e2]),
    )    


class Generator:

    def __init__(self, entities):
        self.faker = Faker()
        self.dataset = { e: [] for e in entities }
        self.execution_thread = _calculate_execution_thread_(entities)

    def generate_first_name(self, **kwargs):
        """
        Generate a first name
        """
        return self.faker.first_name()

    def generate_last_name(self, **kwargs):
        """
        Generate a second name
        """
        return self.faker.last_name()

    def generate_primary_key(self, **kwargs):
        """
        Generates a primary key
        """
        entity = kwargs.get("entity")
        colname = kwargs.get("colname")
        if entity and colname:
            data = self.dataset[entity]
            for pk, d in enumerate(data, 1):
                d[colname] = pk
        else:
            raise Exception("generate_primary_key: Expecting `entity` and `colname`, but were not found")

    def generate_foreign_key(self, **kwargs):
        """
        Generates a foreign key
        """
        entity = kwargs.get("entity")
        colname = kwargs.get("colname")
        _entity = kwargs.get("_entity")
        _colname = kwargs.get("_colname")
        if entity and colname:
            sample = [ 
                ds[colname] for ds in self.dataset[entity] 
            ]
            for d in self.dataset[_entity]:
                d[_colname] = random.choice(sample)
        else:
            raise Exception("generate_foreign_key: Expecting `entity` and `colname`, but were not found")

    def generate_date(self, **kwargs):
        """
        Generate a date between `low` and `high`
        """
        low = kwargs.get("low")
        high = kwargs.get("high")
        if low and high and low < high:
            # Convert the string dates to datetime objects
            low_date = datetime.strptime(low, "%Y-%m-%d")
            high_date = datetime.strptime(high, "%Y-%m-%d")
            delta = high_date - low_date
            random_days = random.randint(0, delta.days)
            random_date = low_date + timedelta(days=random_days)
            return random_date.strftime("%Y-%m-%d")
        raise Exception(f"generate_date: Incorrect arguments: low='{low}', high='{high}'")

    def generate_timestamp(self, **kwargs):
        """
        Generate a timestamp between `low` and `high`
        """
        low = kwargs.get("low")
        high = kwargs.get("high")
        if low and high and low < high:
            start_ts = int(datetime.strptime(low, "%Y-%d-%m %H:%M:%S").timestamp())
            end_ts = int(datetime.strptime(high, "%Y-%d-%m %H:%M:%S").timestamp())
            rand_ts = random.randint(start_ts, end_ts)
            return datetime.fromtimestamp(rand_ts).strftime("%Y-%d-%m %H:%M:%S")
        raise Exception(f"generate_timestamp: Incorrect arguments: low='{low}', high='{high}'")

    def select_record(self, **kwargs):
        """
        Selects a record from `fname`, and returns the `colname`
        """
        pass

    def generate_price(self, **kwargs) -> float:
        """
        Generate a price between `low` and `high`

        **Assumption** - a money is a precision-2 floating point number
        """
        low = kwargs.get("low")
        high = kwargs.get("high")
        if low and high and low < high:
            return round(random.uniform(low, high), 2)
        raise Exception(f"generate_price: Incorrect arguments: low={low}, high={high}")

    def generate_product_name(self, **kwargs) -> str:
        """
        Generate a product name; that is, colour name and a word
        """
        color = self.faker.color_name()
        word = self.faker.word()
        adjective = random.choice(ADJECTIVES)
        return f"{color} {adjective} {word}"

    def generate_non_negative_integer(self, **kwargs):
        """
        Generate a non-negative integer
        """
        low = kwargs.get("low")
        high = kwargs.get("high")
        if low and high and low < high:
            return random.randint(low, high)
        raise Exception(
            f"generate_non_negative_integer: Incorrect arguments: low={low}, high={high}"
        )


def generator_function(g: Generator, fun_name):
    return {
        "generate_first_name": g.generate_first_name,
        "generate_last_name": g.generate_last_name,
        "generate_primary_key": g.generate_primary_key,
        "generate_foreign_key": g.generate_foreign_key,
        "generate_date": g.generate_date,
        "generate_timestamp": g.generate_timestamp,
        "select_record": g.select_record,
        "generate_price": g.generate_price,
        "generate_product_name": g.generate_product_name,
        "generate_non_negative_integer": g.generate_non_negative_integer,
    }.get(fun_name)


def generate_mock_data(entities: Dict) -> List[Dict]:
    """
    Generates mock data according to the configuration in `entities`
    """
    g = Generator(entities)
    dataset = g.dataset
    for e in g.execution_thread:
        ent = entities[e]
        volume = ent["volume"]
        pk, fk = [], []
        for _ in range(1, volume+1):
            res = {}
            schema = ent["schema"]
            for k, v in schema.items():
                use_fn = v.get("use")
                args = v.get("args", {})
                if use_fn  == "generate_primary_key":
                    pk.append(
                        { 
                            "colname": k, 
                            "use_fn": use_fn, 
                            "args": { "entity": e, "colname": k }
                        }
                    )
                elif use_fn == "generate_foreign_key":
                    fk.append(
                        { 
                            "colname": k, 
                            "use_fn": use_fn, 
                            "args": { "_entity": e, "_colname": k, **args }
                        }
                    )
                else:
                    res[k] = generator_function(g, use_fn)(**args) 
            dataset[e].append(res)
        # Create primary-key and foreign-keys
        for pfk in [pk, fk]:
            for k in pfk:
                use_fn = k["use_fn"]
                args = k["args"]
                generator_function(g, use_fn)(**args)
    return dataset

