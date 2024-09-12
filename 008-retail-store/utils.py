"""
Utils module
"""
import json
import yaml
from typing import List, Dict, Union


def read_yaml(fname: str) -> Dict:
    """
    Reads the YAML file `fname`
    """
    try:
        with open(fname, "r") as f:
            return yaml.safe_load(f)
    except FileNotFound as err:
        raise Exception(f"read_yaml: File not found: {fname}: {err}")
    except yaml.YAMLError as err:
        raise Exception(f"read_yaml: YAML error: {fname}: {err}")
    except Exception as err:
        raise Exception(f"read_yaml: general error: {fname}: {err}")


def write_json(data: Union[Dict,List[Dict]], fname: str):
	"""
	Writes to JSON file
	"""
	try:
		with open(fname, "w", encoding="UTF-8") as f:
			json.dump(data, f, indent=4)
	except Exception as err:
		raise Exception(f"write_json: generic error: {fname}")


