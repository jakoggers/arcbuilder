import requests
from bs4 import BeautifulSoup
import json
from categories import pokemon_gender

items_page = requests.get("https://pokemondb.net/item/all")
items_html = BeautifulSoup(items_page.content, "html.parser")

with open("read_items.html", 'w', encoding='utf-8') as read_items:
	read_items.write(str(items_html))

pokemon_item = items_html.find_all('tr')

item_counter = 0
for item in pokemon_item:
	if ">Hold items<" in str(item) or ">Berries<" in str(item):
		find_val = str(item)[4:].find("data-sort-value=")
		find_end = str(item)[4:].find(">")
		print(find_end)
		print("\n" + str(item)[find_val:find_end+1] + "\n")
		item_counter += 1
print(item_counter)

json_categories_location = "json_categories/pokemon_genders.json"

with open(json_categories_location, "w", encoding="utf-8") as write_genders:
	write_genders.write(json.dumps(pokemon_gender, indent=4, ensure_ascii=False))

# init a list
# add to json