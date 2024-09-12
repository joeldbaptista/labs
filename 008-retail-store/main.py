"""
"""
import utils as u
import generators as g

fname = "./configs/retail-store.yml"
entities = u.read_yaml(fname=fname)
data = g.generate_mock_data(entities)

for k,v in data.items():
	u.write_json(v, f"outs/{k}.json")
