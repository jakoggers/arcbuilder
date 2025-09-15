import pandas as pd
import json
import time
from alive_progress import alive_bar
from misc_scraper import lookup_mon

# Read the named csv and a mapped csv
named_pokemon_csv = pd.read_csv("csv_files/Full Team Data.csv")
mapped_pokemon_csv = pd.read_csv("csv_files/mapped_team_data.csv")

# Holds the data of a Pokemon including its mapped moves and items
class PokemonData:
	# evs, ivs, and moves are DICTS
	# , item, gender, ability, level, tera_type, nature, evs, ivs, moves
	moves = {}
	unmapped_moves = {} # Tailwind, Fake out, etc

	def __init__(self):
		self.name = ""
		self.item = ""
		self.gender = ""  # set it depending on the pokemon
		self.ability = ""
		self.level = 50
		self.tera_type = ""  # make it the same as the given pokemon
		self.nature = ""  # random
		self.evs = {
			"ev_hp": 0,
			"ev_attack": 0,
			"ev_defense": 0,
			"ev_special_attack": 0,
			"ev_special_defense": 0,
			"ev_speed": 0,
		}
		self.ivs = {
			"iv_hp": 31,
			"iv_attack": 31,
			"iv_defense": 31,
			"iv_special_attack": 31,
			"iv_special_defense": 31,
			"iv_speed": 31,
		}
		self.moves = {}
		# Unmapped items for easy comparison
		self.umapped_item = ""
		self.unmapped_moves = {}

	def __str__(self):
		return f"Name: {self.name} \nItem: {self.item} \nAbility: {self.ability} \nTera Type: {self.tera_type} \nMoveset: {self.moves}\nGender: {self.gender} \nNature: {self.nature} \nEVs: {self.evs} \nIVs: {self.ivs} "

def modify_name(pokemon_name):
	name_modifications = {
		"gastrodon-east": "gastrodon",
		"gastrodon-west": "gastrodon",
		"giratina": "giratina-altered",
		"indeedee": "indeedee-male",
		"indeedee-f": "indeedee-female",
		"necrozma-dusk-mane": "necrozma-dusk",
		"necrozma-dawn-wings": "necrozma-dawn",
		"ogerpon-wellspring": "ogerpon-wellspring-mask",
		"ogerpon-hearthflame": "ogerpon-hearthflame-mask",
		"ogerpon-cornerstone": "ogerpon-cornerstone-mask",
		"sinistcha-masterpiece": "sinistcha",
		"landorus": "landorus-incarnate",
		"thundurus": "thundurus-incarnate",
		"tornadus": "tornadus-incarnate",
		"meowstic": "meowstic-male",
		"enamorus": "enamorus-incarnate",
		"maushold": "maushold-family-of-three",
		"maushold-four": "maushold-family-of-four",
		"urshifu": "urshifu-single-strike",
		"basculegion": "basculegion-male",
		"tatsugiri": "tatsugiri-curly",
	}

	if pokemon_name in name_modifications:
		pokemon_name = name_modifications.get(pokemon_name)

	if " " in pokemon_name:
		pokemon_name = pokemon_name.replace(" ", "-")

	return pokemon_name

# Check ev's. To see if a Pokemon is fragmented, all its ev's would be 0
def check_fragment():
	ev_sum = 0
	for i in range(4, 10):
		pokemon_ev = mapped_pokemon_csv.iloc[0, i]
		ev_sum += pokemon_ev if pokemon_ev > 0 else 0

	fragmented = True if ev_sum == 0 else False
	return fragmented

def categorize_pkmn(given_pokemon_data, given_pokemon_index):
	given_pokemon_data.name = modify_name(mapped_pokemon_csv.iloc[given_pokemon_index, 0].lower())
	given_pokemon_data.item = mapped_pokemon_csv.iloc[given_pokemon_index, 1]
	given_pokemon_data.ability = mapped_pokemon_csv.iloc[given_pokemon_index, 2]
	given_pokemon_data.nature = mapped_pokemon_csv.iloc[given_pokemon_index, 3]
	given_pokemon_data.moves = {
		"Move 1": mapped_pokemon_csv.iloc[given_pokemon_index, 16],
		"Move 2": mapped_pokemon_csv.iloc[given_pokemon_index, 17],
		"Move 3": mapped_pokemon_csv.iloc[given_pokemon_index, 18],
		"Move 4": mapped_pokemon_csv.iloc[given_pokemon_index, 19],
	}

	"""
	pokemon_moves_named = {
		"Move 1": named_pokemon_csv.iloc[given_pokemon_index, 19],
		"Move 2": named_pokemon_csv.iloc[given_pokemon_index, 18],
		"Move 3": named_pokemon_csv.iloc[given_pokemon_index, 17],
		"Move 4": named_pokemon_csv.iloc[given_pokemon_index, 16],
	}
	"""
	return given_pokemon_data

# Buckets
strength_type = {
	"Bulky": 0,
}
attack_type = {
	"Physical": 0,
	"Special": 0,
}
buckets = {
	"Attacker": 0, # add the attack type for attacker & sweeper
	"Support": 0,
	"Sweeper": 0,
	"Environment": 0,
	"Setup": 0,
	"Status": 0,
	"Tank": 0,
	"Boosting": 0, # wildcard category. if this is the highest, go to the second highest
	"Wall": 0,
	"Wallbreaker": 0,
}
restricted_pokemon = [
	"mewtwo",
	"lugia",
	"ho-oh",
	"kyogre",
	"groudon",
	"rayquaza",
	"dialga",
	"dialga-origin",
	"palkia",
	"palkia-origin",
	"giratina",
	"giratina-origin",
	"reshiram",
	"zekrom",
	"kyurem",
	"cosmog",
	"cosmoem",
	"solgaleo",
	"lunala",
	"necrozma",
	"zacian",
	"zacian-crowned",
	"zamazenta",
	"zamazenta-crowned",
	"eternatus",
	"calyrex",
	"calyrex-glastrier",
	"calyrex-spectrier",
	"koriadon",
	"miraidon",
	"terapagos",
	"terapagos-terastal",
]

# To understand the "Magic Numbers", refer to the txt files in json_categories with the various category
def fragmented_mon(given_pokemon_class_data, given_pokemon_index, write_file):
	title = "Attacker"
	pokemon_types = []
	trick_room_user = ""
	categories = []

	# rank base_stat_total
	try:
		base_stat_total = {}
		with open(f"pokemon_info/{given_pokemon_class_data.name}_data.json", "r", encoding="utf-8") as read_data:
				read_pokemon_data = json.load(read_data)

				for num in range(6):
					stat_name = read_pokemon_data['stats'][num]['stat']['name']
					stat_num = read_pokemon_data['stats'][num]['base_stat']
					base_stat_total[stat_name] = (stat_num) # stat dict = stat base_stat_total

				# Read Types
				for pokemon_type in read_pokemon_data['types']:
					pokemon_types.append(pokemon_type["type"]["name"])

				base_stat_total = sorted(base_stat_total.items(), key=lambda item: item[1], reverse=True)
	except FileNotFoundError as e:
		print(f"Pokemon File for '{given_pokemon_class_data.name}' not found")


	if base_stat_total[0][0] == "special-attack":
		attack_type["Special"] += 1
	elif base_stat_total[0][0] == "attack":
		attack_type["Physical"] += 1

	# Item Check
	named_item = str(named_pokemon_csv.iloc[given_pokemon_index, 1])
	if given_pokemon_class_data.item == 2 or given_pokemon_class_data.item == 0:
		for bucket in buckets:
			buckets[bucket] += 1
		if "Choice " in named_item:
			categories.append(f"{named_item}")
	elif given_pokemon_class_data.item == 3:
		buckets["Wall"] += 1
		buckets["Tank"] += 1

	# Ability Check
	named_ability = str(named_pokemon_csv.iloc[given_pokemon_index, 2])
	if given_pokemon_class_data.ability == 0:
		buckets["Boosting"] += 1
	elif given_pokemon_class_data.ability == 1:
		buckets["Environment"] += 1
		buckets["Support"] += 1
	elif given_pokemon_class_data.ability == 2:
		buckets["Attacker"] += 1
		buckets["Sweeper"] += 1
	elif given_pokemon_class_data.ability == 3:
		buckets["Attacker"] += 1
		buckets["Setup"] += 1
		buckets["Support"] += 1
		buckets["Wall"] += 1
		buckets["Tank"] += 1
	elif given_pokemon_class_data.ability == 4:
		buckets["Wall"] += 1
		buckets["Tank"] += 1
	elif given_pokemon_class_data.ability == 5:
		buckets["Setup"] += 1
		buckets["Status"] += 1
	elif given_pokemon_class_data.ability == 6:
		buckets["Support"] += 1
		buckets["Tank"] += 1
		buckets["Wall"] += 1
	elif given_pokemon_class_data.ability == 7:
		buckets["Support"] += 1
	elif given_pokemon_class_data.ability == 8:
		buckets["Support"] += 1

	# nurture core (me in a field of grass with my face down)
	if given_pokemon_class_data.nature == 1 or given_pokemon_class_data.nature == 5:
		buckets["Attacker"] += 1
		attack_type["Physical"] += 1
	elif given_pokemon_class_data.nature == 2 or given_pokemon_class_data.nature == 4:
		buckets["Setup"] += 1
		buckets["Wall"] += 1
		buckets["Tank"] += 1
		buckets["Status"] += 1
		buckets["Support"] += 1
	elif given_pokemon_class_data.nature == 3:
		buckets["Attacker"] += 1
		attack_type["Special"] += 1

	move_index = 19
	for move in given_pokemon_class_data.moves:
		named_move = str(named_pokemon_csv.iloc[given_pokemon_index, move_index])
		# Physical
		if given_pokemon_class_data.moves[move] == 10:
			attack_type["Physical"] += 1
			buckets["Attacker"] += 1
			buckets["Sweeper"] += 1

		# Special
		elif given_pokemon_class_data.moves[move] == 11:
			attack_type["Special"] += 1
			buckets["Attacker"] += 1
			buckets["Sweeper"] += 1

		elif given_pokemon_class_data.moves[move] == 0 or given_pokemon_class_data.moves[move] == 7:
			for bucket in buckets:
				buckets[bucket] += 1
			buckets["Sweeper"] += 1
			if named_move == "Tailwind":
				categories.append(named_move)
		elif given_pokemon_class_data.moves[move] == 1:
			buckets["Setup"] += 1
			buckets["Wallbreaker"] += 1
		elif given_pokemon_class_data.moves[move] == 2: # check for wide guard
			buckets["Wall"] += 1
			buckets["Setup"] += 1
			buckets["Tank"] += 1
			if named_move == "Wide Guard":
				categories.append(named_move)

		elif given_pokemon_class_data.moves[move] == 3:
			categories.append("Redirector")
			if named_move == "Follow Me" or named_move == "Rage Powder":
				categories.append(named_move)
		elif given_pokemon_class_data.moves[move] == 4: # Specify condition (toxic and shi)
			status_condition_moves = ["Toxic", "Thunder Wave", "Sleep Powder", "Will-O-Wisp", "Spore", "Hypnosis", "Sing", "Glare"]
			buckets["Support"] += 1
		elif given_pokemon_class_data.moves[move] == 5:
			buckets["Support"] += 1
		elif given_pokemon_class_data.moves[move] == 9:
			trick_room_user = "Trick Room"

		if move_index == 22:
			move_index = 19
		else:
			move_index += 1

	write_file.write(f"Attack Type Bucket {attack_type} \n")
	write_file.write(f"General Bucket: {buckets} \n")

	def title(given_dict):
		given_values = list(given_dict.values())
		given_keys = list(given_dict.keys())
		return given_keys[given_values.index(max(given_values))]

	title = f"{title(attack_type)} {title(buckets)}"

	categories.append(trick_room_user)
	categories = categories
	categories.append(title)

	write_file.write(str(categories))
	write_file.write(f"\n{trick_room_user}{title} \n \n")

	for bucket in buckets:
		buckets[bucket] = 0

	for attack in attack_type:
		attack_type[attack] = 0

	pokemon_types = []
	# print(f"{max(attack_type.values(), key=attack_type.get)} {max(buckets.values(), key=buckets.get)}")

def print_info(given_pokemon_class_data, write_file, given_pokemon_index):
	write_file.write(f"Name: {given_pokemon_class_data.name} \n")
	lookup_mon(given_pokemon_class_data.name, write_file)
	write_file.write(f"\nItem: {given_pokemon_class_data.item}; {named_pokemon_csv.iloc[given_pokemon_index, 1]} \n")
	write_file.write(f"Ability: {given_pokemon_class_data.ability}; {named_pokemon_csv.iloc[given_pokemon_index, 3]} \n")
	write_file.write(f"Nature: {given_pokemon_class_data.nature}; {named_pokemon_csv.iloc[given_pokemon_index, 6]} \n")
	write_file.write(f"Move 1: {given_pokemon_class_data.moves["Move 1"]}; {named_pokemon_csv.iloc[given_pokemon_index, 19]} \n")
	write_file.write(f"Move 2: {given_pokemon_class_data.moves["Move 2"]}; {named_pokemon_csv.iloc[given_pokemon_index, 20]} \n")
	write_file.write(f"Move 3: {given_pokemon_class_data.moves["Move 3"]}; {named_pokemon_csv.iloc[given_pokemon_index, 21]} \n")
	write_file.write(f"Move 4: {given_pokemon_class_data.moves["Move 4"]}; {named_pokemon_csv.iloc[given_pokemon_index, 22]} \n")

if __name__ == "__main__":
	with open("data_analysis/test_categories", 'w', encoding='utf-8') as write_categories:
		wat_time = time.time()
		with alive_bar(7284) as bar:
			for given_pokemon_index in range(7284):

				pokemon_data = categorize_pkmn(PokemonData(), given_pokemon_index)
				print_info(pokemon_data, write_categories, given_pokemon_index)
				if check_fragment:
					fragmented_mon(pokemon_data, given_pokemon_index, write_categories)
				bar()
	print(f"Completed Data Write Time in {time.time() - wat_time}")
