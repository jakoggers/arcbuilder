#imports
import requests, json
from bs4 import BeautifulSoup
from teams import pokemon_team

def ev_and_iv_organizer(pokemon_num, ev_or_iv, which_one):
	find_char = ev_or_iv.index(":")
	findWspace = ev_or_iv.index("\n")
	evLine = ev_or_iv[find_char + 2:findWspace - 2].split("/") # slice the line by its slashes
	for i in range(len(evLine)): # remove the white space
		evLine[i] = evLine[i].strip()
	for stat_change in evLine: # use the method to filter and add the evs
		match stat_change:
			case stat_change if "HP" in stat_change:
				hp = stat_change[:len(stat_change) - 3].strip()
				pokemon_team[pokemon_num][which_one + "-hp"] = hp
				# print("The HP ev in question: " + hp)
			case stat_change if "Atk" in stat_change:
				attack = stat_change[:len(stat_change) - 3].strip()
				pokemon_team[pokemon_num][which_one + "-attack"] = attack
				#print("The Attack ev in question: " + attack)
			case stat_change if "Def" in stat_change:
				defense = stat_change[:len(stat_change) - 3].strip()
				pokemon_team[pokemon_num][which_one + "-defense"] = defense
				#print("The Defense ev in question: " + defense)
			case stat_change if "SpA" in stat_change:
				special_attack = stat_change[:len(stat_change) - 3].strip()
				pokemon_team[pokemon_num][which_one + "-special attack"] = special_attack
				#print("The Special Attack ev in question: " + special_attack)
			case stat_change if "SpD" in stat_change:
				special_defense = stat_change[:len(stat_change) - 3].strip()
				pokemon_team[pokemon_num][which_one + "-special defense"] = special_defense
				#print("The Special Defense ev in question: " + special_defense)
			case stat_change if "Spe" in stat_change:
				speed = stat_change[:len(stat_change) - 3].strip()
				pokemon_team[pokemon_num][which_one + "-speed"] = speed
				#print("The Speed ev in question: " + speed)
	# print(ev_or_iv)

# to function!
def write_team_data(given_link): # write this to Pokemon Folder link
	with open(given_link) as f:
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
					pokemon_team[which_pokemon]["name"] = name
					pokemon_team[which_pokemon]["item"] = item

				# Write ability:
				case read_line if "Ability: " in read_line:
					find_char = read_line.index(":")
					ability = read_line[find_char + 2:].strip()
					pokemon_team[which_pokemon]["ability"] = ability

				# Write Level:
				case read_line if "Level: " in read_line:
					find_char = read_line.index(":")
					level = read_line[find_char:].strip()
					pokemon_team[which_pokemon]["level"] = level

				# Write Tera Type:
				case read_line if "Tera Type: " in read_line:
					find_char = read_line.index(":")
					tera_type = read_line[find_char + 2:].strip()
					pokemon_team[which_pokemon]["tera type"] = tera_type

				# Write Nature:
				case read_line if "Nature" in read_line:
					find_char = read_line.index("Nature")
					nature = read_line[:find_char].strip()
					pokemon_team[which_pokemon]["nature"] = nature

				# Write EVs
				case read_line if "EVs: " in read_line:
					ev_and_iv_organizer(which_pokemon, read_line, "ev")

				# Write IVs
				case read_line if "IVs:" in read_line:
					ev_and_iv_organizer(which_pokemon, read_line, "iv")

				# Write in all moves:
				case read_line if "-" in read_line: #given lineis a move
					find_char = read_line.index("-")
					move_name = read_line[find_char + 2:].strip()
					pokemon_team[which_pokemon]["move-" + str(move_counter)] = move_name
					move_counter += 1

			read_line = f.readline()

# Give it a pokepaste
def team_handler(get_url, file_name):
	# pokepaste link !!!!!!

	# get the url from pokepaste
	page = requests.get(get_url)
	link_to_pokemon_team_folder = "pokemon_teams/" + file_name + ".txt"

	# The txt file we're gonna work from
	newPokemonFile = open(link_to_pokemon_team_folder, "w")

	# opens a new file, writes the html of the site to the page
	htmlPokemon = open("newPokemonTeam.html", "w")
	htmlPokemon.write(page.text)


	# Utilizing BeautifulSoup, take all pokemon data and parse it.
	soup = BeautifulSoup(page.content, "html.parser")
	pokemon_stats = soup.find_all("pre")
	for stat in pokemon_stats:
		newPokemonFile.write(stat.text + "\n")

	#------------- organize the data -------------------------------------------------------
	newPokemonFile = open(link_to_pokemon_team_folder, "w")

	# Writes all team_data
	write_team_data(link_to_pokemon_team_folder)

	# dumps it into JSON (might remove later)
	#readable_dict = open("jakoggerTeam.json", "w")
	#readable_dict.write(json.dumps(pokemon_team, indent=4, ensure_ascii=False))

	# Close all the files, memory management type shiii >:)
	#readable_dict.close()
	newPokemonFile.close()
	htmlPokemon.close()

	print(f"File: {file_name} written!")




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
""" counter = 0
for poggermon in pokemon_team:
	readable_dict.write("Pokemon " + str(counter + 1))
	readable_dict.write("\n")
	for key, value in poggermon.items():
		readable_dict.write(f"{key}: {value}")
		readable_dict.write("\n")
	readable_dict.write("\n")
	counter += 1 """