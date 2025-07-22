import requests
from bs4 import BeautifulSoup
import json
from categories import pokemon_genders
import pandas as pd
data = pd.read_csv("Full Team Data.csv")

team_csv = pd.DataFrame(data)

team_csv = team_csv.drop(columns= ['level', 'gender'])

"""
# map the entire list column to ints, based on their order
list_of_items = team_csv['item'].tolist()
enumerate_sorted_set = enumerate(sorted(set(list_of_items)))
items_dict = {}
for num, item in enumerate_sorted_set:
	items_dict[item] = f'{num}'

team_csv['item'] = team_csv['item'].map(items_dict)

"""

team_csv.to_csv("misc/mapped_items.csv", encoding="utf-8", index=False)
print("csv'd items")


# make it more general
# create a list of all items
# add a category to each
# go back and mark them all with the number
# {0: consumalbes, 1: boosting, 2: protective}

items_page = requests.get("https://pokemondb.net/item/all")
items_html = BeautifulSoup(items_page.content, "html.parser")

with open("misc/read_items.html", 'w', encoding='utf-8') as read_items:
	read_items.write(str(items_html))

pokemon_item = items_html.find_all('td')

item_counter = 0
for item in pokemon_item:
	print(item)

	find_val = str(item)[4:].find("data-sort-value=")
	find_end = str(item)[4:].find(">")
	print(find_end)
	print("\n" + str(item)[find_val:find_end+1] + "\n")
	item_counter += 1

print(item_counter)

"""
with open("json_categories/count of each.txt", 'a') as write_freq:
	write_freq.write(str(pokemon_counts))


"""

# print(team_csv)
#print(pokemon_counts)


"""






json_categories_location = "json_categories/pokemon_genders.json"

with open(json_categories_location, "w", encoding="utf-8") as write_genders:
	write_genders.write(json.dumps(pokemon_gender, indent=4, ensure_ascii=False))

"""




# init a list
# add to json


# [1, 2, 2, 3, 4, 5, 5, 6]