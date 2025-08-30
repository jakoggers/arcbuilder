import pandas as pd
import json

named_pokemon_csv = pd.read_csv("csv_files/Full Team Data.csv")
mapped_pokemon_csv = pd.read_csv("csv_files/mapped_team_data.csv")

class PokemonData:
	# evs, ivs, and moves are DICTS
	# , item, gender, ability, level, tera_type, nature, evs, ivs, moves
	name = ""
	item = ""
	ability = ""
	level = 50
	tera_type = ""
	default_gender = ""
	default_evs = {
			"ev_hp": 0,
			"ev_attack": 0,
			"ev_defense": 0,
			"ev_special_attack": 0,
			"ev_special_defense": 0,
			"ev_speed": 0,
		}
	default_ivs = {
			"iv_hp": 31,
			"iv_attack": 31,
			"iv_defense": 31,
			"iv_special_attack": 31,
			"iv_special_defense": 31,
			"iv_speed": 31,
		}
	moves = {}

	def __init__(self, name, item, ability, nature, moves, tera_type = tera_type, gender = default_gender, evs = default_evs, ivs = default_ivs):
		self.name = name
		self.item = item
		self.gender = gender  # set it depending on the pokemon
		self.ability = ability
		self.level = "50"
		self.tera_type = tera_type  # make it the same as the given pokemon
		self.nature = nature  # random
		self.evs = evs
		self.ivs = ivs
		self.moves = moves

	def __str__(self):
		return f"Name: {self.name} \nItem: {self.item} \nAbility: {self.ability} \nTera Type: {self.tera_type} \nMoveset: {self.moves}\nGender: {self.gender} \nNature: {self.nature} \nEVs: {self.evs} \nIVs: {self.ivs} "

def modify_name(pokemon_name):
	name_modifications = {
		"gastrodon-east": "gastrodon",
		"gastrodon-west": "gastrodon",
		"indeedee-f": "indeedee-female",
		"necrozma-dusk-mane": "necrozma-dusk",
		"necrozma-dawn-wings": "necrozma-dawn",
		"ogerpon-wellspring": "ogerpon-wellspring",
		"ogerpon-hearthflame": "ogerpon-hearthflame",
		"ogerpon-cornerstone": "ogerpon-cornerstone-mask",
		"sinistcha-masterpiece": "sinistcha"
	}

	if pokemon_name in name_modifications:
		pokemon_name = name_modifications.get(pokemon_name)

	if " " in pokemon_name:
		pokemon_name = pokemon_name.replace(" ", "-")
		print(pokemon_name)

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
		"Move 1": mapped_pokemon_csv.iloc[given_pokemon_index, 19],
		"Move 2": mapped_pokemon_csv.iloc[given_pokemon_index, 18],
		"Move 3": mapped_pokemon_csv.iloc[given_pokemon_index, 17],
		"Move 4": mapped_pokemon_csv.iloc[given_pokemon_index, 16],
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
trick_room = {
	"Trick Room": False, # Automatically adds trick room to Pokemon Category if it's found
}
attack_type = {
	"Physical": 0,
	"Special": 0,
}
buckets = {
	"Attacker": 0, # add the attack type for attacker & sweeper
	"Sweeper": 0,
	"Environment": 0,
	"Redirection": 0,
	"Setup": 0,
	"Status": 0,
	"Boosting": 0, # wildcard category. if this is the highest, go to the second highest
	"Wall": 0,
	"Wallbreaker": 0,
	"Distruption": 0,
	"Healing": 0,
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

def fragmented_mon(given_pokemon_class_data):
	title = "Attacker"
	# rank base_stat_total
	try:
		base_stat_total = {}
		with open(f"pokemon_info/{given_pokemon_class_data.name}_data.json", "r", encoding="utf-8") as read_data:
				read_pokemon_data = json.load(read_data)

				for num in range(6):
					stat_name = read_pokemon_data['stats'][num]['stat']['name']
					stat_num = read_pokemon_data['stats'][num]['base_stat']
					base_stat_total[stat_name] = (stat_num) # stat dict = stat base_stat_total
				base_stat_total = sorted(base_stat_total.items(), key=lambda item: item[1], reverse=True)
	except FileNotFoundError as e:
		print(f"Pokemon File for '{given_pokemon_class_data.name}' not found")


	if base_stat_total[0][0] == "special-attack":
		attack_type["Special"] += 1
	elif base_stat_total[0][0] == "attack":
		attack_type["Physical"] += 1

	if given_pokemon_class_data.item == 2 or given_pokemon_class_data.item == 0:
		for bucket in buckets:
			buckets[bucket] += 1
	elif given_pokemon_class_data.item == 3:
		buckets["Wall"] += 1

	# Ability Check
	if given_pokemon_class_data.ability == 0:
		buckets["Boosting"] += 1
	elif given_pokemon_class_data.ability == 1:
		buckets["Environment"] += 1
	elif given_pokemon_class_data.ability == 2:
		buckets["Attacker"] += 1
		buckets["Sweeper"] += 1
	elif given_pokemon_class_data.ability == 3:
		buckets["Attacker"] += 1
		buckets["Setup"] += 1
	elif given_pokemon_class_data.ability == 4:
		buckets["Wall"] += 1
	elif given_pokemon_class_data.ability == 5:
		buckets["Setup"] += 1
		buckets["Status"] += 1

	# nurture core (me in a field of grass with my face down)
	if given_pokemon_class_data.nature == 1 or given_pokemon_class_data.nature == 5:
		buckets["Attacker"] += 1
		buckets["Sweeper"] += 1
		attack_type["Physcial"] += 1
	elif given_pokemon_class_data.nature == 2 or given_pokemon_class_data.nature == 4:
		buckets["Setup"] += 1
		buckets["Wall"] += 1
		buckets["Status"] += 1
	elif given_pokemon_class_data.nature == 3:
		buckets["Attacker"] += 1
		buckets["Sweeper"] += 1
		attack_type["Special"] += 1

	for move in given_pokemon_class_data.moves:
		if given_pokemon_class_data.moves[move] == 11:
			buckets["Attacker"] += 1

	print(attack_type)
	print(buckets)

	def title(given_dict):
		given_values = list(given_dict.values())
		given_keys = list(given_dict.keys())
		return given_keys[given_values.index(max(given_values))]

	title = f"{title(attack_type)} {title(buckets)}"

	print(title)
	# print(f"{max(attack_type.values(), key=attack_type.get)} {max(buckets.values(), key=buckets.get)}")

def print_info(given_pokemon_class_data):
	print("Name:", given_pokemon_class_data.name)
	print("Item:", given_pokemon_class_data.item)
	print("Ability:", given_pokemon_class_data.ability)
	print("Nature:", given_pokemon_class_data.nature)
	print("Move 1:", given_pokemon_class_data.moves["Move 1"])
	print("Move 2:", given_pokemon_class_data.moves["Move 2"])
	print("Move 3:", given_pokemon_class_data.moves["Move 3"])
	print("Move 4:", given_pokemon_class_data.moves["Move 4"])

if __name__ == "__main__":
	for given_pokemon_index in range(10):
		pokemon_data = categorize_pkmn(PokemonData(
			modify_name(mapped_pokemon_csv.iloc[given_pokemon_index, 0].lower()), # name
			mapped_pokemon_csv.iloc[given_pokemon_index, 1], # item
			mapped_pokemon_csv.iloc[given_pokemon_index, 2], # ability
			mapped_pokemon_csv.iloc[given_pokemon_index, 3], # nature
			{
				"Move 1": mapped_pokemon_csv.iloc[given_pokemon_index, 19],
				"Move 2": mapped_pokemon_csv.iloc[given_pokemon_index, 18],
				"Move 3": mapped_pokemon_csv.iloc[given_pokemon_index, 17],
				"Move 4": mapped_pokemon_csv.iloc[given_pokemon_index, 16],
			}
			), given_pokemon_index)
		print_info(pokemon_data)
		if check_fragment:
			fragmented_mon(pokemon_data)