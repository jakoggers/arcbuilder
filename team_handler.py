# imports
import requests, json
from bs4 import BeautifulSoup
from teams import pokemon_team_structure
from algo import run_algo

def ev_and_iv_organizer(pokemon_num, ev_or_iv, which_one, given_pokemon_team):
	find_char = ev_or_iv.index(":")
	find_wspace = ev_or_iv.index("\n")
	ev_line = ev_or_iv[find_char + 2:find_wspace - 2].split("/") # slice the line by its slashes
	for i in range(len(ev_line)): # remove the white space
		ev_line[i] = ev_line[i].strip()
	for stat_change in ev_line: # use the method to filter and add the evs
		match stat_change:
			case stat_change if "HP" in stat_change:
				hp = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][which_one + "_hp"] = hp
				# print("The HP ev in question: " + hp)
			case stat_change if "Atk" in stat_change:
				attack = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][which_one + "_attack"] = attack
				#print("The Attack ev in question: " + attack)
			case stat_change if "Def" in stat_change:
				defense = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][which_one + "_defense"] = defense
				#print("The Defense ev in question: " + defense)
			case stat_change if "SpA" in stat_change:
				special_attack = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][which_one + "_special_attack"] = special_attack
				#print("The Special Attack ev in question: " + special_attack)
			case stat_change if "SpD" in stat_change:
				special_defense = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][which_one + "_special_defense"] = special_defense
				#print("The Special Defense ev in question: " + special_defense)
			case stat_change if "Spe" in stat_change:
				speed = int(stat_change[:len(stat_change) - 3].strip())
				given_pokemon_team[pokemon_num][which_one + "_speed"] = speed
				#print("The Speed ev in question: " + speed)
	# print(ev_or_iv)

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
					# For every pokemon, initialize the value given in the section
					given_pokemon_team[which_pokemon]["name"] = name
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
					given_pokemon_team[which_pokemon]["tera type"] = tera_type

				# Write Nature:
				case read_line if "Nature" in read_line:
					find_char = read_line.index("Nature")
					nature = read_line[:find_char].strip()
					given_pokemon_team[which_pokemon]["nature"] = nature

				# Write EVs
				case read_line if "EVs: " in read_line:
					ev_and_iv_organizer(which_pokemon, read_line, "ev", given_pokemon_team)

				# Write IVs
				case read_line if "IVs:" in read_line:
					ev_and_iv_organizer(which_pokemon, read_line, "iv", given_pokemon_team)

				# Write in all moves:
				case read_line if "-" in read_line: #given lineis a move
					find_char = read_line.index("-")
					move_name = read_line[find_char + 2:].strip()
					given_pokemon_team[which_pokemon]["move_" + str(move_counter)] = move_name
					move_counter += 1

			read_line = f.readline()

			with open(given_json_location, "w", encoding="utf-8") as write_json:
				write_json.write(json.dumps(given_pokemon_team, indent=4, ensure_ascii=False))

# Give it a pokepaste
def team_handler(get_url, file_name):
	# Assumes ALL teams have 6 pokemon
	#monitor_file = open("misc/monitor_file", "w", encoding="utf-8")
	# get the url from pokepaste
	print(f"\nFile I'm working with: {file_name}.txt \n")

	page = requests.get(get_url)
	create_team_file = "pokemon_teams/" + file_name + ".txt"
	create_team_json = f"pokemon_team_jsons/{file_name}_JSON.json"

	# Utilizing BeautifulSoup, take all pokemon data and parse it.
	soup = BeautifulSoup(page.content, "html.parser")
	pokemon_stats = soup.find_all("pre")

	# Write the Team Data into the given Text file:
	print(f"Writing into: {create_team_file}")
	newPokemonFile = open(create_team_file, "w", encoding="utf-8")
	for stat in pokemon_stats:
		newPokemonFile.write(stat.text + "\n")
	newPokemonFile.close()

	#------------- organize the data -------------------------------------------------------

	# Writes all team_data into a JSON file
	print(f"Writing JSON into: {create_team_json} from {create_team_file}")
	write_team_data(create_team_file, create_team_json, pokemon_team_structure)
	# Close all the files, memory management type shiii >:)
	#print("Algorithm Results: ")
	#run_algo(create_team_json)

	print(f"\nFile: {file_name} written! No problems (hopefully)")

	#monitor_file.close()

# Test Teams:
"""
	https://pokepast.es/46e426ed62136f59 // made by hsxd_snakob himself
	https://pokepast.es/ef6920d4f30db897 // made by idk
	https://pokepast.es/722a7a53b4f46592 - made by
	https://pokepast.es/84c0b7c14de37a87 // portland champion team, scarvi regulation I: centered around Kyogre
	https://pokepast.es/8a2335a101620d91 // team around ho-oh
	https://pokepast.es/5ee3277dc45acb8c // team around zamazenta
"""

# Call organize data function!!!!
# organize_data()

# Write dictionary VALUES as a txt file