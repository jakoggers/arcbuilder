#imports
import requests, json
from bs4 import BeautifulSoup
from teams import pokemon_team_structure

# doubles team from '23
getURL = "https://pokepast.es/46e426ed62136f59"

"""
	https://pokepast.es/46e426ed62136f59 // made by hsxd_snakob himself
	https://pokepast.es/ef6920d4f30db897 // made by idk
	https://pokepast.es/722a7a53b4f46592 - made by
"""

page = requests.get(getURL)

newPokemonFile = open("z_test_data.txt", "w") # The txt file we're gonna work from

soup = BeautifulSoup(page.content, "html.parser")

pokemon_stats = soup.find_all("pre") # in the pokepaste, it takes all the pokemon data!!!!
for stat in pokemon_stats:
	newPokemonFile.write(stat.text + "\n")
	# print(stat) # print stats

#------------- organize the data -------------------------------------------------------
newPokemonFile = open("z_team.txt", "r")
#for key, value in pokemon1.items():
#	print(key, value)

def ev_and_iv_organizer(ev_or_iv, which_one):
	find_char = ev_or_iv.index(":")
	findWspace = ev_or_iv.index("\n")
	evLine = ev_or_iv[find_char + 2:findWspace - 2].split("/") # slice the line by its slashes
	for i in range(len(evLine)): # remove the white space
		evLine[i] = evLine[i].strip()
	for stat_change in evLine: # use the method to filter and add the evs
		match stat_change:
			case stat_change if "HP" in stat_change:
				hp = stat_change[:len(stat_change) - 3].strip()
				pokemon_team_structure[which_pokemon][which_one + "-hp"] = hp
				# print("The HP ev in question: " + hp)
			case stat_change if "Atk" in stat_change:
				attack = stat_change[:len(stat_change) - 3].strip()
				pokemon_team_structure[which_pokemon][which_one + "-attack"] = attack
				#print("The Attack ev in question: " + attack)
			case stat_change if "Def" in stat_change:
				defense = stat_change[:len(stat_change) - 3].strip()
				pokemon_team_structure[which_pokemon][which_one + "-defense"] = defense
				#print("The Defense ev in question: " + defense)
			case stat_change if "SpA" in stat_change:
				special_attack = stat_change[:len(stat_change) - 3].strip()
				pokemon_team_structure[which_pokemon][which_one + "-special attack"] = special_attack
				#print("The Special Attack ev in question: " + special_attack)
			case stat_change if "SpD" in stat_change:
				special_defense = stat_change[:len(stat_change) - 3].strip()
				pokemon_team_structure[which_pokemon][which_one + "-special defense"] = special_defense
				#print("The Special Defense ev in question: " + special_defense)
			case stat_change if "Spe" in stat_change:
				speed = stat_change[:len(stat_change) - 3].strip()
				pokemon_team_structure[which_pokemon][which_one + "-speed"] = speed
				#print("The Speed ev in question: " + speed)
	# print(ev_or_iv)
with open('z_team.txt') as f:
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
				pokemon_team_structure[which_pokemon]["name"] = name
				pokemon_team_structure[which_pokemon]["item"] = item

			case read_line if "Ability: " in read_line:
				find_char = read_line.index(":")
				ability = read_line[find_char + 2:].strip()
				pokemon_team_structure[which_pokemon]["ability"] = ability

			case read_line if "Level: " in read_line:
				find_char = read_line.index(":")
				level = read_line[find_char:].strip()
				pokemon_team_structure[which_pokemon]["level"] = level

			case read_line if "Tera Type: " in read_line:
				find_char = read_line.index(":")
				tera_type = read_line[find_char + 2:].strip()
				pokemon_team_structure[which_pokemon]["tera type"] = tera_type

			case read_line if "Nature" in read_line:
				find_char = read_line.index("Nature")
				nature = read_line[:find_char].strip()
				pokemon_team_structure[which_pokemon]["nature"] = nature

			case read_line if "EVs: " in read_line:
				ev_and_iv_organizer(read_line, "ev")

			case read_line if "IVs:" in read_line:
				ev_and_iv_organizer(read_line, "iv")

			case read_line if "-" in read_line: #given lineis a move
				find_char = read_line.index("-")
				move_name = read_line[find_char + 2:].strip()
				pokemon_team_structure[which_pokemon]["move-" + str(move_counter)] = move_name
				move_counter += 1

		read_line = f.readline()

readable_dict = open("pokemon_team_structure.json", "w")
readable_dict.write(json.dumps(pokemon_team_structure, indent=4, ensure_ascii=False))
print("JSON'd the file yo!")

readable_dict.close()
newPokemonFile.close()
htmlPokemon.close()

# Write dictionary VALUES as a txt file
counter = 0
for poggermon in pokemon_team_structure:
	readable_dict.write("Pokemon " + str(counter + 1))
	readable_dict.write("\n")
	for key, value in poggermon.items():
		readable_dict.write(f"{key}: {value}")
		readable_dict.write("\n")
	readable_dict.write("\n")
	counter += 1