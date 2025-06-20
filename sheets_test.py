import gspread

# my KEY!!!!! i should private this.....
gc = gspread.api_key("AIzaSyCganQ_Z_uzJVKIPcUs0Dleoo7e07mzcEo")


sh = gc.open_by_key("1axlwmzPA49rYkqXh7zHvAtSP-TKbM0ijGYBPRflLSWw")

current_regulation = sh.worksheet("SV Regulation I")

list_of_teams = current_regulation.col_values(25)

regulation_name = "sv_regulation_I"

def write_all_teams():
	with open(f"{regulation_name}_teams.txt", "w") as f:
		# loop through all teams, and write them into the file
		for team in list_of_teams:
			f.write(team + "\n")
		print(f"\"Every team at the palm of my hands\": Pokepastes, written into file \"{regulation_name}_teams.txt\"")

write_all_teams()