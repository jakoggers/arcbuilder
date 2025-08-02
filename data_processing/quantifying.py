# Turn all abilities, items, and moves into numbers
def categorize_list(given_list, given_dictionary):
	with open(given_list, 'r') as read_category:
		given_lines = read_category.readlines()

		group = 0

		for line in given_lines:
			line = line.strip()
			current_num = str(line)[0]

			if ord(current_num) != 45:
				group = int(current_num)
				continue

			remove_hyphen = line.index("-") + 1
			category_name = line[remove_hyphen:].strip()
			given_dictionary[category_name] = group

	#with open("json_categories/pokemon_abilities.json", "w", encoding="utf-8") as write_json:
	#	write_json.write(json.dumps(given_dictionary, indent=4, ensure_ascii=False))

	return given_dictionary


def categorize_moves(list_of_moves, given_dict):
	with open(list_of_moves, 'r', encoding="utf-8") as read_moves:
		given_moves = read_moves.readlines()

		for line in given_moves:
			find_name = line.index(':') + 1
			move_name = line[find_name:line.index('|')].strip()

			# remaining values AFTER status moves have been updated
			if "Physical" in line:
				given_dict['physical'][move_name] = 10
			elif "Special" in line:
				given_dict['special'][move_name] = 11

		return given_dict

#abilites_dict = {}
#print(categorize_JSON(categorized_list_location, abilites_dict))
#print("Categorized!")