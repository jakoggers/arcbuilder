import gspread
from config import google_api_key
from team_handler import team_handler

# my KEY!!!!! i should private this.....
gc = gspread.api_key(google_api_key)


sh = gc.open_by_key("1axlwmzPA49rYkqXh7zHvAtSP-TKbM0ijGYBPRflLSWw")

current_regulation = sh.worksheet("SV Regulation I")

team_description = current_regulation.col_values(2)
list_of_teams = current_regulation.col_values(25)

regulation_name = "sv_regulation_I"
file_name = regulation_name + "_teams.txt"


def write_all_teams():
	with open(file_name, "w") as sheet_to_txt:
		# loop through all teams, and write them into the file
		for team in list_of_teams:
			# remove any whitespace & other words
			if team == "":
				continue
			if team == "Pokepaste":
				continue
			sheet_to_txt.write(f"\"{team}\"\n")
		print(f"\"Every team at the palm of my hands\": Pokepastes, written into file \"{regulation_name}_teams.txt\"")

# After writing all the teams, turn each file into a txt
def pokemon_to_txt(file):
	with open(file, "r") as link_to_txt:
		file_number = 0
		# Every file, each as a text file
		for link in link_to_txt:
			team_handler(link, str(file_number))
			file_number += 1
		print("Data has been withdrawn. All files in folder: \"pokemon_teams\"")

# team_handler("https://pokepast.es/937d52cf84a051de", str(5))

write_all_teams()
pokemon_to_txt(file_name)

# For later: add the team name to doc?
"""
batchget = current_regulation.batch_get(['B:B', 'Y:Y'])

for team in batchget:
	print(f"Team: {team}")

for name, team in batchget:
	print(f"Name: {name}; Team Link: {team}")
"""

