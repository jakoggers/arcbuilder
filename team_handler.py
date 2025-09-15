# imports
import requests, json
import os
import pandas as pd
import random as rd
import copy
from bs4 import BeautifulSoup
from teams import pokemon_team_structure

#makes this faster fr
with open("json_categories/pokemon_genders.json", 'r') as read_genders:
	pokemon_gender = json.load(read_genders)

class DataErrors:
	def __init__(self):
		self.errors = []

	def add_error(self, given_json_file, given_paste, pokemon, field, error):
		self.errors.append({
			"JSON File Location": given_json_file,
			"Link to Paste": given_paste,
			"Pokemon": pokemon,
			"Field": field,
			"Error": error
		})

	def printed_report(self):
		if not self.errors:
			# print("No errors found!")
			return

		final_errors = {
			"errors": self.errors,
			"Total Errors:": len(self.errors)
		}

		with open("error_checking/error_list.json", "a+", encoding="utf-8") as write_json:
			json.dump(final_errors, write_json, indent=2, ensure_ascii=False)

		print(f"Errors: {len(self.errors)}")

# because ev's and iv's can be parsed the same way initalizing both depending on the input
def ev_and_iv_organizer(given_line, given_pokemon_team, pokemon_num, chosen_stat):
	# just so i dont have any magic numbers
	find_char = given_line.index(":") + 2
	find_wspace = given_line.index("\n") - 2

	ev_line = given_line[find_char:find_wspace].split("/") # slice the line by its slashes

	for i in range(len(ev_line)): # remove the white space
		ev_line[i] = ev_line[i].strip()
		print(ev_line[i])
	for stat_change in ev_line: # use the method to filter and add the evs
		find_stat_change = len(stat_change) - 3
		find_stat_name = stat_change[find_stat_change:].strip()
		given_stat = int(stat_change[:find_stat_change].strip())

		

		stat_name = {
				"HP": "hp",
				"Atk": "attack",
				"Def": "defense",
				"SpA": "special_attack",
				"SpD": "special_defense",
				"Spe": "speed"
			}

		if find_stat_name in stat_name:
			given_pokemon_team[pokemon_num][f"{chosen_stat}s"][f"{chosen_stat}_{stat_name[find_stat_name]}"] = given_stat
		else:
			print(f"Invalid stat! @{given_pokemon_team} @ {given_pokemon_team[pokemon_num]} @ {pokemon_num}")
			return


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

	find_last_lparan = name.rfind("(")
	find_last_rparan = name.rfind(")")

	find_gender = name[find_last_lparan:find_last_rparan + 1]
	has_gender = find_gender in ["(M)", "(F)"]

	if has_gender or name.strip().endswith(")"):
		check_nick = name.strip()
		find_nick_lparan = check_nick.index("(") + 1
		find_nick_rparan = check_nick.index(")")
		final_name = check_nick[find_nick_lparan:find_nick_rparan].strip()

		if final_name in ["F", "M"]: # Final check! I know it's a band-aid solution BUT it works for now. Unless someone at Pokepaste decides to mess with it smh.
			find_first_left_paran = name.index("(")
			final_name = name[:find_first_left_paran].strip()
	else:
		final_name = name.strip()

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
	team_errors = DataErrors()
	with open(given_link, 'r+', encoding="utf-8") as f:
		# read every indiviual line
		lines = f.readlines()

		move_counter = 1 # specifically increment through moves 1 by 1
		which_pokemon = -1; # increment through the list

		for read_line in lines:
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
					find_char = read_line.index(":") + 2
					ability = read_line[find_char:].strip()
					given_pokemon_team[which_pokemon]["ability"] = ability

				# Write Level:
				case read_line if "Level: " in read_line:
					find_char = read_line.index(":") + 2
					level = int(read_line[find_char:].strip())
					given_pokemon_team[which_pokemon]["level"] = level

				# Write Tera Type:
				case read_line if "Tera Type: " in read_line:
					find_char = read_line.index(":") + 2
					tera_type = read_line[find_char:].strip()
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
					find_char = read_line.index("-") + 2
					move_name = read_line[find_char:].strip()
					given_pokemon_team[which_pokemon]["moves"]["move_" + str(move_counter)] = move_name
					move_counter += 1

		# One last look through
		for num in range(len(given_pokemon_team)):
			if given_pokemon_team[num]["name"] in {"Ditto", "Unown", "Cosmog", "Cosmoem", "Gimmighoul"}: # Specific list of pokemon with < 1 move
				for i in range(1, 5):
					if given_pokemon_team[num]["moves"]["move_" + str(i)] == "":
						given_pokemon_team[num]["moves"]["move_" + str(i)] = "Blank" # a ngeligible category later on!!!

			# There's people who forget... and have HORRIBLE syntax smh
			elif given_pokemon_team[num]["name"] == "Calyrex-Ice" or given_pokemon_team[num]["name"] == "Calyrex-Shadow" and given_pokemon_team[num]["ability"] == "":
				given_pokemon_team[num]["ability"] = "As One"

			elif given_pokemon_team[num]["name"] == "Ursaluna-Bloodmoon":
				given_pokemon_team[num]["ability"] = "Mind's Eye"

			# Error check everything else :)
			for category in given_pokemon_team[num]:
				if given_pokemon_team[num]["nature"] == "":
					given_pokemon_team[num]["nature"] = "Blank"
				elif given_pokemon_team[num][category] == "":
					team_errors.add_error(given_json_location, given_link, given_pokemon_team[num]["name"], category, "Blank")

		team_errors.printed_report()
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
	"""
	print(f"\nFile I'm working with: {file_name}.txt \n")
	print(f"Writing into: {create_team_file}")
	print(f"Writing JSON into: {create_team_json} from {create_team_file}")
	print(f"\nFile: {file_name} written! No problems (hopefully)")
	"""

	# Utilizing BeautifulSoup, take all pokemon data and parse it.
	soup = BeautifulSoup(page.content, "html.parser")
	pokemon_stats = soup.find_all("pre")

	# Write the Team Data into the given Text file:
	newPokemonFile = open(create_team_file, "w", encoding="utf-8")
	with open(create_team_file, "w", encoding="utf-8") as write_pokemon_txt:

		for stat in pokemon_stats:
			write_pokemon_txt.write(stat.text + "\n")
		"""
		scan = write_pokemon_txt.readlines()

		mon_counter = 0
		for mon in scan:
			if "@" in mon:
				mon_counter += 1

		if mon_counter != 6:
			print("Skipped. Pokemon count is: ", mon_counter)
			return"""

	#------------- organize the data -------------------------------------------------------
	# Writes all team_data into a JSON file
	def new_team():
		return copy.deepcopy(pokemon_team_structure)

	write_team_data(create_team_file, create_team_json, new_team())
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
		try:
			with open(json_to_read, "r", encoding="utf-8") as open_json:
				json_data = json.load(open_json)
				flattened_json = pd.json_normalize(json_data)
				rows_to_csv.append(flattened_json)
		except FileNotFoundError as e:
			print(f"Error: {e}, @ {i}_JSON moving on. (File doesn't exist because I cut the JSON)")
			continue

	fused_json = pd.concat(rows_to_csv, ignore_index=False)
	fused_json = fused_json.reset_index(drop=True)

	fused_json.to_csv("csv_files/Full Team Data.csv", encoding="utf-8", index=False)
	# clean the data, bruh whose idea was it to clean the data like this smh... making it O(n)^2... what a geek
	print("CSV'd the file gangana!!!!")

# Really weird error with a certain Ursalnua's abiility written as Mind’s Eye rather than Mind's Eye