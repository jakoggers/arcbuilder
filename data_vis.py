import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

import os

from config import local_teamjson_path
json_path = os.path.basename(local_teamjson_path)
test_file = f"{json_path}/3_JSON.json"
test_file_2 = f"{json_path}/4_JSON.json"


# print(tera_types)

sns.set_theme()
tips = sns.load_dataset("tips")
"""
sns.relplot(
	data = tips,
	x="total_bill", y="tip", col="time",
	hue="smoker", style="smoker",size="size",
)

tera_types = read_json_file["tera_type"]
iv_column = read_json_file["ivs"][3]
"""
# plt.show()


with open(test_file, "r") as first_json:
	read_json_file = pd.read_json(test_file)
	data = json.load(first_json)

with open(test_file_2, "r") as next_json:
	read_next_json_file = pd.read_json(test_file_2)
	next_data = json.load(next_json)

flattened_json = pd.json_normalize(data)
next_flattened_json = pd.json_normalize(next_data)

fused_json = pd.concat([flattened_json, next_flattened_json])



print(fused_json)
fused_json.to_csv(f"full_team_data.csv", encoding="utf-8", index=False)
print("CSV'd the file gangana!!!!")


#print(flattened_json)
# print(flattened_json)

#flattened_json.to_csv(f"full_team_data.csv", encoding="utf-8", index=False)

#print(new_json)
#print(flat)


# print(new_json)