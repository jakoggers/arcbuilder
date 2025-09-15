import gspread
from config import google_api_key, sheets_key, local_file_path, local_teamfile_path
from team_handler import team_handler
import os
from alive_progress import alive_it

filename_path = os.path.basename(local_file_path)
team_folder_path = os.path.basename(local_teamfile_path)

# my KEY!!!!! i should private this.....
gc = gspread.api_key(google_api_key)

sh = gc.open_by_key(sheets_key)

current_regulation = sh.worksheet("SV Regulation I")

team_description = current_regulation.col_values(2)
list_of_teams = current_regulation.col_values(25)


def write_all_teams():
	with open(filename_path, "w") as sheet_to_txt:
		# loop through all teams, and write them into the file
		for team in list_of_teams:
			# remove any whitespace & other words
			if team == "":
				continue
			if team == "Pokepaste":
				continue
			sheet_to_txt.write(f"{team}\n")
		print(f"\"Every team at the palm of my hands\": Pokepastes, written into file \"{filename_path}\"")


# After writing all the teams, turn each file into a txt
def pokemon_to_txt(file):

	with open(file, "r+", encoding="utf-8") as read_file:
		bar = alive_it(enumerate(read_file))
		for team_number, link in bar:
			team_handler(link.strip(), str(team_number)) # this line took me 10 hours to fix and it was just a strip() call.
			bar.text("Works~!")
	print(f"Data has been withdrawn. All files in folder: \"{team_folder_path}/\"")


# For later: add the team name to doc?
"""
batchget = current_regulation.batch_get(['B:B', 'Y:Y'])

for team in batchget:
	print(f"Team: {team}")

for name, team in batchget:
	print(f"Name: {name}; Team Link: {team}")
"""

