import json

# Turn all abilities, items, and moves into numbers
categorized_list_location = "json_categories/items.txt"
abilites_dict = {}
def categorize_JSON(given_list, given_dictionary):
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


print(categorize_JSON(categorized_list_location, abilites_dict))
print("Categorized!")