import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
data = pd.read_csv("Full Team Data.csv")

page = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_moves")
soup = BeautifulSoup(page.content, "html.parser")

with open("json_categories/items.html", "a", encoding="utf-8") as write_moves:
	# write_moves.write(soup.prettify())
	pass

moves = soup.find("table")
block = moves.find_all("td")
names = block[0].find_all("a")

physical_moves = {}

moves_list = {}


with open("json_categories/moves_list.txt", "w+", encoding="utf-8") as moves_file:
	names = names[6:]
	num_lines = 0
	for i in range(0, len(names), 4):
		move = names[i].text.strip()
		category = names[i + 2].text.strip()
		if category in {"Physical", "Special", "Status"}:

			# Depending on the generation, adding various cases depening on the move
			if move == "Nature Power":
				moves_file.write(f"Move: {move} | Category: Special \n")
			else:
				moves_file.write(f"Move: {move} | Category: {category} \n")

		if category == "???": # Checks for Max and Z-Moves
			if "Max" in move:
				moves_file.write(f"Move: {move} | Category: Max Move \n")
			else:
				moves_file.write(f"Move: {move} | Category: Z-Move \n")

		num_lines += 1





		#if move_or_cat == "Physical" or move_or_cat == "Special" or move_or_cat == "Status":
		#	moves_file.write(f"Move Category: {move_or_cat} \n")
print("Written!")
	#elif i % 4 == 0:
	#	print("Move Category: ", names[i].text.strip())

# make it more general
# create a list of all items
# add a category to each
# go back and mark them all with the number
# {0: consumalbes, 1: boosting, 2: protective}


"""


item_counter = 0
for item in pokemon_item:
	print(item)

	find_val = str(item)[4:].find("data-sort-value=")
	find_end = str(item)[4:].find(">")
	print(find_end)
	print("\n" + str(item)[find_val:find_end+1] + "\n")
	item_counter += 1

"""

# print(team_csv)
#print(pokemon_counts)


"""
json_categories_location = "json_categories/pokemon_genders.json"


# map the entire list column to ints, based on their order
list_of_items = team_csv['item'].tolist()
enumerate_sorted_set = enumerate(sorted(set(list_of_items)))
items_dict = {}
for num, item in enumerate_sorted_set:
	items_dict[item] = f'{num}'

team_csv['item'] = team_csv['item'].map(items_dict)



with open("misc/read_items.txt", 'w', encoding='utf-8') as read_items:
	read_items.write(str(items_html))


"""