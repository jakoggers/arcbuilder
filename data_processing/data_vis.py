import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from quantifying import categorize_JSON

# Turn all abilities, items, and moves into numbers

categorized_abilities_path = "json_categories/abilities.txt"
categorized_items_path = "json_categories/items.txt"
categorized_natures_path = "json_categories/natures.txt"
dict_organizer = {}

map_abilities = categorize_JSON(categorized_abilities_path, dict_organizer)
map_items = categorize_JSON(categorized_items_path, dict_organizer)
map_natures = categorize_JSON(categorized_natures_path, dict_organizer)

data = pd.read_csv("Full Team Data.csv")

team_csv = pd.DataFrame(data)

team_csv = team_csv.drop(columns= ['level', 'gender', 'tera_type'])

list_of_abilities = team_csv['ability'].tolist()
team_csv['ability'] = team_csv['ability'].map(map_abilities)

list_of_items = team_csv['item'].tolist()
team_csv['item'] = team_csv['item'].map(map_items)

list_of_natures = team_csv['nature'].tolist()
team_csv['nature'] = team_csv['nature'].map(map_natures)

print("Categorized!")

team_csv.to_csv("misc/mapped_team_data.csv", encoding="utf-8", index=False)
print("csv'd ")
print(team_csv.shape)
print(team_csv.columns)
