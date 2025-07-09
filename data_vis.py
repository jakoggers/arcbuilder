import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

from config import local_teamjson_path
json_path = os.path.basename(local_teamjson_path)


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
list_of_jsons = os.listdir("pokemon_team_jsons")
num_of_jsons = len(list_of_jsons)

"""
# O(n) time.... smh # incorrect solution, this didn't clean add the files to the csv efficiently...
for i in range(num_of_jsons - 1):
	test_file = f"{json_path}/{i}_JSON.json"
	test_file_2 = f"{json_path}/{i + 1}_JSON.json"

	with open(test_file, "r", encoding="utf-8") as first_json:
		read_json_file = pd.read_json(test_file)
		data = json.load(first_json)

	with open(test_file_2, "r", encoding="utf-8") as next_json:
		read_next_json_file = pd.read_json(test_file_2)
		next_data = json.load(next_json)

	flattened_json = pd.json_normalize(data)
	next_flattened_json = pd.json_normalize(next_data)
	fused_json = pd.concat([flattened_json, next_flattened_json])
	fused_json.to_csv(f"full_team_data.csv", mode="a+", encoding="utf-8", index=False)
"""
rows_to_csv = []
for i in range(num_of_jsons):
	json_to_read = f"{json_path}/{i}_JSON.json"

	with open(json_to_read, "r", encoding="utf-8") as open_json:
		json_data = json.load(open_json)
		flattened_json = pd.json_normalize(json_data)
		rows_to_csv.append(flattened_json)

fused_json = pd.concat(rows_to_csv, ignore_index=False)
fused_json = fused_json.reset_index(drop=True)

fused_json.to_csv("full_team_data.csv", encoding="utf-8", index=False)

# clean the data, bruh whose idea was it to clean the data like this smh... making it O(n)^2... what a geek
print("CSV'd the file gangana!!!!")


#print(flattened_json)
# print(flattened_json)

#flattened_json.to_csv(f"full_team_data.csv", encoding="utf-8", index=False)

#print(new_json)
#print(flat)


# print(new_json)