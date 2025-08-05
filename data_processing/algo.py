

"""

if pokemon_info:
	for i in range(6):
		print(f"Stat Name: {pokemon_info["stats"][i]['stat']['name']}; Value: {pokemon_info["stats"][i]['base_stat']}")

	print(f"Num of Types: {len(pokemon_info["types"])}")
	for pokemon_type in range(len(pokemon_info["types"])):
		print(f"Type: {pokemon_info["types"][pokemon_type]['type']['name']}")

	print(f"Num of Abilities: {len(pokemon_info["abilities"])}")
	for pokemon_ability in range(len(pokemon_info["abilities"])):
		print(f"Type: {pokemon_info["abilities"][pokemon_ability]['ability']['name']}")

	for move in range(len(pokemon_info["moves"])):
		print(f"Move {move}: {pokemon_info["moves"][move]['move']['name']}") # check n

	print()
"""



	# Stat Name: {pokemon_info["stats"][i]['stat']['name']}; Value: {pokemon_info["stats"][i]['base_stat']} - pull stats

def run_algo(given_json):
		with open(given_json, "r", encoding="utf-8") as calc_json:
			for line in calc_json:
				print(line, end='')