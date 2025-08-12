import pandas as pd
import json

pokemon_csv = pd.read_csv("csv_files/mapped_team_data.csv")

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

# Check ev's. To see if a Pokemon is fragmented, all its ev's would be 0


ev_sum = 0
for i in range(4, 10):
	pokemon_ev = pokemon_csv.iloc[0, i]
	ev_sum += pokemon_ev if pokemon_ev > 0 else 0

fragmented = True if ev_sum == 0 else False


pokemon_name = pokemon_csv.iloc[0, 0].lower()
pokemon_item = pokemon_csv.iloc[0, 1]
pokemon_ability = pokemon_csv.iloc[0, 2]
pokemon_nature = pokemon_csv.iloc[0, 3]
pokemon_moves = {
	"Move 1": pokemon_csv.iloc[0, 19],
	"Move 2": pokemon_csv.iloc[0, 18],
	"Move 3": pokemon_csv.iloc[0, 17],
	"Move 4": pokemon_csv.iloc[0, 16],
}

if pokemon_name in name_modifications:
	pokemon_name = name_modifications.get(pokemon_name)

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
if fragmented is True:
	# rank base_stat_total
	base_stat_total = {}
	with open(f"pokemon_info/{pokemon_name}_data.json", "r", encoding="utf-8") as read_data:
		read_pokemon_data = json.load(read_data)

		for num in range(6):
			stat_name = read_pokemon_data['stats'][num]['stat']['name']
			stat_num = read_pokemon_data['stats'][num]['base_stat']
			base_stat_total[stat_name] = (stat_num) # stat dict = stat base_stat_total
		base_stat_total = sorted(base_stat_total.items(), key=lambda item: item[1], reverse=True)

	if base_stat_total[0][0] == "special-attack":
		attack_type["Special"] += 1
		if pokemon_item == 2 or pokemon_item ==0:
			buckets["Attacker"] += 1
		if pokemon_ability == 0:
			buckets["Boosting"] += 1
		elif pokemon_ability == 1:
			buckets["Environment"] += 1
		elif pokemon_ability == 2:
			buckets["Attacker"] += 1
			buckets["Sweeper"] += 1
		elif pokemon_ability == 3:
			buckets["Attacker"] += 1
			buckets["Setup"] += 1
		elif pokemon_ability == 4:
			buckets["Wall"] += 1
		elif pokemon_ability == 5:
			buckets["Setup"] += 1
			buckets["Status"] += 1
	elif base_stat_total[0][0] == "attack":
		attack_type["Physcial"] += 1
	for move in pokemon_moves:
		if pokemon_moves[move] == 11:
			buckets["Attacker"] += 1
	print(attack_type)
	print(buckets)

	def title(given_dict):
		given_values = list(given_dict.values())
		given_keys = list(given_dict.keys())
		return given_keys[given_values.index(max(given_values))]

	print(title(attack_type), title(buckets))
	# print(f"{max(attack_type.values(), key=attack_type.get)} {max(buckets.values(), key=buckets.get)}")

