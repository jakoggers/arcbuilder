import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from quantifying import categorize_list, categorize_moves

# Load all mappings from respective locations
categorized_abilities_path = "json_categories/abilities.txt"
categorized_items_path = "json_categories/items.txt"
categorized_natures_path = "json_categories/natures.txt"
categorized_moves_location = "json_categories/moves.txt"
categorized_status_moves_location = "json_categories/moves_status.txt"


physical_moves = {}
special_moves = {}

moves_organizer = {
	"physical": physical_moves,
	"special": special_moves
}

map_abilities = categorize_list(categorized_abilities_path, {})
map_items = categorize_list(categorized_items_path, {})
map_natures = categorize_list(categorized_natures_path, {})
map_status_moves = categorize_list(categorized_status_moves_location, {})
map_attacking_moves = categorize_moves(categorized_moves_location, moves_organizer)
merge_moves = map_status_moves | physical_moves | special_moves



team_csv = pd.read_csv("csv_files/Full Team Data.csv")

team_csv = team_csv.drop(columns= ['level', 'gender', 'tera_type'])

column_names = list(team_csv.columns)
names_to_json = ['abilities', 'items', 'natures', 'moves']
dicts_to_json = [map_abilities, map_items, map_natures, merge_moves]
for i in range(len(names_to_json)):
	with open(f"json_categories/pokemon_{names_to_json[i]}.json", 'w', encoding="utf-8") as write_maps:
		json.dump(dicts_to_json[i], write_maps, indent=4)

list_of_abilities = team_csv['ability'].tolist()
team_csv['ability'] = team_csv['ability'].map(map_abilities)

list_of_items = team_csv['item'].tolist()
team_csv['item'] = team_csv['item'].map(map_items)

list_of_natures = team_csv['nature'].tolist()
team_csv['nature'] = team_csv['nature'].map(map_natures)

list_of_moves1 = team_csv['moves.move_1'].to_list()
team_csv['moves.move_1'] = team_csv['moves.move_1'].map(merge_moves)

list_of_moves2 = team_csv['moves.move_2'].to_list()
team_csv['moves.move_2'] = team_csv['moves.move_2'].map(merge_moves)

list_of_moves3 = team_csv['moves.move_3'].to_list()
team_csv['moves.move_3'] = team_csv['moves.move_3'].map(merge_moves)

list_of_moves4 = team_csv['moves.move_4'].to_list()
team_csv['moves.move_4'] = team_csv['moves.move_4'].map(merge_moves)

print("Categorized!")

# Check null
#na_df = team_csv.isna()

team_csv.to_csv("csv_files/mapped_team_data.csv", encoding="utf-8", index=False)
test_tree = team_csv.to_csv("csv_files/mapped_team_data_no_name.csv", encoding="utf-8", index=False)
print(f"csv'd over {int(len(team_csv)/ 6)} teams")
print(team_csv.shape)
print(column_names)
