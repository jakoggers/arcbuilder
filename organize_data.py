import json
import os

#def organize_data():
# Loading the prompt list:
with open("prompts.json", "r") as team:
	given_team = json.load(team)

output = []

for i, entry in enumerate(given_team):
	file_path = f"pokemon_teams/{i}.txt"

	# if the file path doesn't exist, display message stating that it's missing a prompt at a certain path
	if not os.path.exists(file_path):
		print(f"Missing a response for prompt {i}: , {entry}")
		continue

	# read the file and remove all whitespace
	with open(file_path, "r") as readfile:
		response = readfile.read().strip()

	output.append({
		"prompt": entry,
		"response": response
	})

# save as a json file
with open("training_data.json", "w") as openFile:
	# for each prompt, write in the file
	for pair in output:
		openFile.write(json.dumps(pair) + "\n")