# imports
import requests, json
import os
import pandas as pd
import random as rd
from bs4 import BeautifulSoup
from teams import pokemon_team_structure

# because ev's and iv's can be parsed the same way initalizing both depending on the input
def ev_and_iv_organizer(given_line, given_pokemon_team, pokemon_num, chosen_stat):
	find_char = given_line.index(":")
	find_wspace = given_line.index("\n")
	ev_line = given_line[find_char + 2:find_wspace - 2].split("/") # slice the line by its slashes
	for i in range(len(ev_line)): # remove the white space
		ev_line[i] = ev_line[i].strip()
	for stat_change in ev_line: # use the method to filter and add the evs
		match stat_change:
			case stat_change if "HP" in stat_change:
				hp = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][f"{chosen_stat}s"][f"{chosen_stat}_hp"] = hp
				# print("The HP ev in question: " + hp)
			case stat_change if "Atk" in stat_change:
				attack = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][f"{chosen_stat}s"][f"{chosen_stat}_attack"] = attack
				#print("The Attack ev in question: " + attack)
			case stat_change if "Def" in stat_change:
				defense = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][f"{chosen_stat}s"][f"{chosen_stat}_defense"] = defense
				#print("The Defense ev in question: " + defense)
			case stat_change if "SpA" in stat_change:
				special_attack = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][f"{chosen_stat}s"][f"{chosen_stat}_special_attack"] = special_attack
				#print("The Special Attack ev in question: " + special_attack)
			case stat_change if "SpD" in stat_change:
				special_defense = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][f"{chosen_stat}s"][f"{chosen_stat}_special_defense"] = special_defense
				#print("The Special Defense ev in question: " + special_defense)
			case stat_change if "Spe" in stat_change:
				speed = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][f"{chosen_stat}s"][f"{chosen_stat}_speed"] = speed
				#print("The Speed ev in question: " + speed)
	# print(given_line)

# check if the parsed name has a name or a gender, checking parentheses
def gender_or_nickname(name, given_pokemon_team, which_pokemon):
	# Set genders of all pokemon
	# find if it has a nickame
	# Check if there are more than two left parentheses
	# If theres one, that means there's either a nickname or gender
		# Add a gender if the len of it equals 3
		# If not, make it equal the name within
	# If there's two, that means there's both
		# At first position, take the name and add to "name"
		# At second left-paran, check gender and add to "gender"

	# parse parentheses
	paran_count = name.count("(")
	find_last_lparan = name.rfind("(")
	find_last_rparan = name.rfind(")")

	find_gender = name[find_last_lparan:find_last_rparan + 1]
	has_gender = find_gender in ["(M)", "(F)"]

	# Strip the trailing space or remove the name
	if has_gender:
		final_name = name[:find_last_lparan].strip()
	else:
		final_name = name.strip()

	with open("json_categories/pokemon_genders.json", 'r') as read_genders:
		pokemon_gender = json.load(read_genders)
	get_gender = pokemon_gender.get(final_name.lower()) # lower to directly compare

	if has_gender:
		if find_gender == "(M)":
			given_pokemon_team[which_pokemon]["gender"] = "Male"
		elif find_gender == "(F)":
			given_pokemon_team[which_pokemon]["gender"] = "Female"

	else:
		if get_gender:
			#print(f"Name w/ specific gender: {name}, Gender: {get_gender}")
			given_pokemon_team[which_pokemon]["gender"] = get_gender
		else:
			# If neither, add the name AND specified gender immediately
			# ok ik there's like a ratio, but for simplicity i'm gonna 50/50 everything that ISN'T specified
			get_gender = rd.choice(["Male", "Female"])
			given_pokemon_team[which_pokemon]["gender"] = get_gender
			#print(f"Name w/o specified gender: {name}, Gender: {get_gender}")

	given_pokemon_team[which_pokemon]["name"] = final_name

# write this to Pokemon Folder link
def write_team_data(given_link, given_json_location, given_pokemon_team):
	# Assumes EVERY Pokemon holds an item
	with open(given_link, 'r+', encoding="utf-8") as f:
		# read every indiviual line
		read_line = f.readline()
		move_counter = 1 # specifically increment through moves 1 by 1
		which_pokemon = -1; # increment through the list

		while read_line:
			match read_line:
				case read_line if "@" in read_line:
					# every new pokemon, increment
					which_pokemon += 1
					move_counter = 1 # resets moves at the name
					find_char = read_line.index("@")
					name = read_line[:find_char].strip()
					item = read_line[find_char + 2:].strip()
					gender_or_nickname(name, given_pokemon_team, which_pokemon)
					given_pokemon_team[which_pokemon]["item"] = item

				# Write ability:
				case read_line if "Ability: " in read_line:
					find_char = read_line.index(":")
					ability = read_line[find_char + 2:].strip()
					given_pokemon_team[which_pokemon]["ability"] = ability

				# Write Level:
				case read_line if "Level: " in read_line:
					find_char = read_line.index(":")
					level = int(read_line[find_char + 2:].strip())
					given_pokemon_team[which_pokemon]["level"] = level

				# Write Tera Type:
				case read_line if "Tera Type: " in read_line:
					find_char = read_line.index(":")
					tera_type = read_line[find_char + 2:].strip()
					given_pokemon_team[which_pokemon]["tera_type"] = tera_type

				# Write Nature:
				case read_line if "Nature" in read_line:
					find_char = read_line.index("Nature")
					nature = read_line[:find_char].strip()
					given_pokemon_team[which_pokemon]["nature"] = nature

				# Write EVs
				case read_line if "EVs: " in read_line:
					ev_and_iv_organizer(read_line, given_pokemon_team, which_pokemon, "ev")

				# Write IVs
				case read_line if "IVs:" in read_line:
					ev_and_iv_organizer(read_line, given_pokemon_team, which_pokemon, "iv")

				# Write in all moves:
				case read_line if "-" in read_line: #given lineis a move
					find_char = read_line.index("-")
					move_name = read_line[find_char + 2:].strip()
					given_pokemon_team[which_pokemon]["moves"]["move_" + str(move_counter)] = move_name
					move_counter += 1

			read_line = f.readline()

			with open(given_json_location, "w", encoding="utf-8") as write_json:
				write_json.write(json.dumps(given_pokemon_team, indent=4, ensure_ascii=False))

# Give it a pokepaste
def team_handler(get_url, file_name):
	# Assumes ALL teams have 6 pokemon
	#monitor_file = open("misc/monitor_file", "w", encoding="utf-8")
	# get the url from pokepaste

	page = requests.get(get_url)
	create_team_file = "pokemon_teams/" + file_name + ".txt"
	create_team_json = f"pokemon_team_jsons/{file_name}_JSON.json"

	print(f"\nFile I'm working with: {file_name}.txt \n")
	print(f"Writing into: {create_team_file}")
	print(f"Writing JSON into: {create_team_json} from {create_team_file}")
	print(f"\nFile: {file_name} written! No problems (hopefully)")

	# Utilizing BeautifulSoup, take all pokemon data and parse it.
	soup = BeautifulSoup(page.content, "html.parser")
	pokemon_stats = soup.find_all("pre")

	# Write the Team Data into the given Text file:
	newPokemonFile = open(create_team_file, "w", encoding="utf-8")
	for stat in pokemon_stats:
		newPokemonFile.write(stat.text + "\n")
	newPokemonFile.close()

	#------------- organize the data -------------------------------------------------------
	# Writes all team_data into a JSON file
	write_team_data(create_team_file, create_team_json, pokemon_team_structure)
	# Close all the files, memory management type shiii >:)

# Compile every team into a readable csv file
def team_to_csv(given_json_path):
	json_path = os.path.basename(given_json_path)
	list_of_jsons = os.listdir("pokemon_team_jsons")
	num_of_jsons = len(list_of_jsons)

	print(json_path)

	rows_to_csv = []
	for i in range(num_of_jsons):
		json_to_read = f"{json_path}/{i}_JSON.json"

		with open(json_to_read, "r", encoding="utf-8") as open_json:
			json_data = json.load(open_json)
			flattened_json = pd.json_normalize(json_data)
			rows_to_csv.append(flattened_json)

	fused_json = pd.concat(rows_to_csv, ignore_index=False)
	fused_json = fused_json.reset_index(drop=True)

	fused_json.to_csv("Full Team Data.csv", encoding="utf-8", index=False)
	# clean the data, bruh whose idea was it to clean the data like this smh... making it O(n)^2... what a geek
	print("CSV'd the file gangana!!!!")
