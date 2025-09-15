import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

# scrape poke api
import requests
import json
import os

data = pd.read_csv("csv_files/Full Team Data.csv")

# For Move List scraping
page = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_moves")
soup = BeautifulSoup(page.content, "html.parser")
moves = soup.find("table")
block = moves.find_all("td")
names = block[0].find_all("a")
base_url = "https://pokeapi.co/api/v2/"

def add_types():
	csv_name = "csv_files/Full Team Data.csv"
	data.to_csv(csv_name, index=False)
	add_types_csv = pd.read_csv(csv_name)

	list_of_types = []

	for pokemon in range():
		types = ""
		pokemon_name = add_types_csv.iloc[pokemon, 0]


	# add_types_csv.insert(1, 'type', list_of_types)
	print(list_of_types)
	print("Types Added!")
# add_types()



# For pokemon name scraping prototype 1 (before you i found a better optoion)
"""
all_pkmn_link = requests.get("https://pokemondb.net/pokedex/national")
pkmn_soup = BeautifulSoup(all_pkmn_link.content, "html.parser")
list_of_pkmn = []
pokemon_names = pkmn_soup.find_all("a", class_='ent-name')
for name in pokemon_names:
	legal_name = name.text.strip().lower()
	if ' ' in legal_name and ':' not in legal_name and '.' not in legal_name:
		legal_name = legal_name.replace(" ", "-")
	if ':' in legal_name:
		legal_name = legal_name.replace(": ", "-")
	if '.' in legal_name:
		legal_name = legal_name.replace(". ", "-")
	if "'" in legal_name:
		legal_name = legal_name.replace("'", "")
	if legal_name == "nidoran♀":
		legal_name = "nidoran-m"
	if legal_name == "nidoran♂":
		legal_name = "nidoran-f"
	if legal_name == "mime jr.":
		legal_name = "mime-jr"
	if legal_name == "flabébé":
		legal_name = "flabebe"
	list_of_pkmn.append(legal_name)
"""


def get_pokemon_info(name):
	find_pokemon = f"{base_url}/pokemon-species/{name}"
	print(f"Finding {find_pokemon}.")
	response = requests.get(find_pokemon)
	if response.status_code == 200:
		pokemon_data = response.json()
		return pokemon_data
	else:
		print(f"Failed. Marked in random_errors.txt")
		with open("random_errors.txt", "a", encoding="utf-8") as error_txt:
			error_txt.write(
				 f"Failed. Code: {response.status_code} on Pokemon: {name} \n"
			)


def get_pokemon_from_link(given_form_link):
	response = requests.get(given_form_link)
	if response.status_code == 200:
		pokemon_data = response.json()
		return pokemon_data
	else:
		with open("random_errors.txt", "a", encoding="utf-8") as error_txt:
			error_txt.write(
				f"Failed. Code: {response.status_code} on Pokemon: {given_form_link} \n"
			)
		print(f"Failed. Marked in random_errors.txt")



def scrape_pokemon_data():
	# print("Testing")
	test_list = [
	 202,
	 386,
	 475,
	 648,
	 800,
	 1000,
	 1017,
	]# Respectively, Wobbuffet, Deoxys, Gallade, Meloetta, Necrozma, Gholdengo, Ogerpon. Wobbuffet and Gholdengo both only have one form, while Ogerpon/Deoxys both have two

	# FOr all the pokemon, write from 1-1026 (Bulbasaur->Pecharunt)
	for number in range(1, 1026):
		pokemon_info = get_pokemon_info(number)
		name = pokemon_info["name"]
		# list is print(f"{name} has more than 1 form.")
		for form in pokemon_info["varieties"]:
			form_name = form["pokemon"]["name"]
			form_link = form["pokemon"]["url"]
			# print(f"Name: {form_name}, Link: {form_link}")
			with open(f'pokemon_info/{form_name}_data.json', 'w+', encoding="utf-8") as pokemon_info_json:
				print(f"Finding {form_name}.")
				form_data = get_pokemon_from_link(form_link)
				json.dump(form_data, pokemon_info_json, indent=4)
	# pokemon_info[key][value]

	# print(f"Wrote {pokemon_name}.json into pokemon_info/{pokemon_name}_data.json!")

	# Write ALL 1000 Pokemon into a singular folder and pull data from there, making the write time/speed faster
	path = 'pokemon_info'
	files = []
	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path, file)):
			files.append(file)

	# Print all the files found
	print(f"Found {len(files)} files in {path}:")
	all_names = []
	for file in files:
		name_by_itself_data_index = str(Path(file).stem).find("_data")
		name_by_itself = str(Path(file).stem)[:name_by_itself_data_index].strip()
		all_names.append(name_by_itself)

	hyphenated_pkmn = data.iloc[:, 0]
	# print(hyphenated_pkmn)
	list_of_hyphenated_pokemon = []
	for i in range(len(hyphenated_pkmn)):
		individual_name = data.iloc[i, 0].lower()
		#and individual_name not in list_of_pkmn and individual_name not in {}
		if "-" in individual_name and individual_name not in all_names:
			list_of_hyphenated_pokemon.append(individual_name)
	new_list_of_hyphenated_pokemon = set(list_of_hyphenated_pokemon)
	for check_name in new_list_of_hyphenated_pokemon:
		print(check_name)



	for pokemon_name in new_list_of_hyphenated_pokemon:
		with open(f'pokemon_info/{pokemon_name}_data.json', 'w', encoding="utf-8") as pokemon_info_json:
				pokemon_info = get_pokemon_info(pokemon_name)
				json.dump(pokemon_info, pokemon_info_json, indent=4)
				print(f"Wrote {pokemon_name}.json into pokemon_info/{pokemon_name}_data.json!")


	with open("species-forms.txt", 'r', encoding="utf-8") as errors:
		pkmn_name = ""
		read_errors = errors.readlines()
		for error_name in read_errors:
			find_end = error_name.rfind(":") + 1
			pkmn_name = error_name[find_end:].strip()
			print(pkmn_name)

	# If name in random_errors, that mean's it's in the species category, as there are multiple forms of it.

	# if name in the specific list with various forms, open up the varieties tab in their pokemon-species and then scrape each url from "url"

def scrape_moves():
	with open("json_categories/moves_list.txt", "w+", encoding="utf-8") as moves_file:
		names = names[6:] # Cut out
		num_lines = 0
		for i in range(0, len(names), 4):
			move = names[i].text.strip()
			category = names[i + 2].text.strip()
			if category in {"Physical", "Special", "Status"}:
				# Depending on the generation, adding various cases depening on the move
				if move == "Nature Power":
					moves_file.write(f"Move: {move} | Category: Special \n")
				elif move == "Blank":
					moves_file.write(f"Move: {move} | Category: Status \n")
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

# elif i % 4 == 0:
# 	print("Move Category: ", names[i].text.strip())

# make it more general
# create a list of all items
# add a category to each
# go back and mark them all with the number
# {0: consumalbes, 1: boosting, 2: protective}

# print(team_csv)
# print(pokemon_counts)


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

def map_files():
	indexd = pd.read_csv("csv_files/mapped_team_data.csv")
	ability_original = data["ability"]

	ability_category_names = [
		"immunity",
		"environmental",
		"boosting_or_debuffing",
		"modifying",
		"protective",
		"preventative",
		"bonding",
		"info",
		"healing",
	]

	for i in range(9):
		try:
			with open(
				f"data_analysis/ability_analysis/{ability_category_names[i]}.txt", "w", encoding="utf-8"
			) as write_immunity:
				immunity = indexd.loc[indexd["ability"] == i]
				abilities = []
				for index, category in immunity.iterrows():
					write_immunity.write(f"At index: {index} Name: {category['name']}, Ability Category: {category['ability']}, Ability Name: {ability_original[index]} \n")
					abilities.append(str(ability_original[index]))
				write_immunity.write(f"Set of Abilities: {set(abilities)}")

				print(f"{ability_category_names[i]} category column written!")
		except FileNotFoundError as e:
			print("File not found. Error", e)

def lookup_mon(given_pokemon, given_write_file):
	with open(f"pokemon_info/{given_pokemon}_data.json", "r", encoding="utf-8") as read_data:
		pokemon_types = []
		read_pokemon_data = json.load(read_data)

		base_stat_total = {}
		for num in range(6):
			stat_name = read_pokemon_data['stats'][num]['stat']['name']
			stat_num = read_pokemon_data['stats'][num]['base_stat']
			base_stat_total[stat_name] = (stat_num) # stat dict = stat base_stat_total

		base_stat_total = sorted(base_stat_total.items(), key=lambda item: item[1], reverse=True)
		highest_stat = list(base_stat_total)[0]
		second_highest_stat = list(base_stat_total)[1]
		lowest_stat = list(base_stat_total)[5]
		second_lowest_stat = list(base_stat_total)[4]

		for pokemon_type in read_pokemon_data['types']:
			pokemon_types.append(pokemon_type["type"]["name"])

		given_write_file.write(f"Stats: {pokemon_types} \n")
		given_write_file.write(f"Highest Stat: {highest_stat} \n")
		given_write_file.write(f"Second highest Stat: {second_highest_stat} \n")
		given_write_file.write(f"Lowest Stat: {lowest_stat} \n")
		given_write_file.write(f"Second Lowest Stat: {second_lowest_stat} \nBase Stats: \n")
		given_write_file.write(str(base_stat_total))

		pokemon_types = []

"""
if __name__ == "__main__":
	group = ["iron-hands", "ursaluna", "torkoal", "ursaluna-bloodmoon", "calyrex-ice", "lunala", "groudon", "kyogre"]
	for pokemon in group:
		lookup_mon(pokemon) """