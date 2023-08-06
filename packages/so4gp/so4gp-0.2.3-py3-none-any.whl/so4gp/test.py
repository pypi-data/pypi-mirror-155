from src.so4gp import so4gp

out_json, gps = so4gp.acogps('DATASET.csv', max_iteration=20, return_gps=True)
print(out_json)

import json
out_obj = json.loads(out_json)
print(out_obj["Invalid Count"])
