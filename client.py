import os
from config import local_file_path, local_teamjson_path
from team_to_txt import write_all_teams, pokemon_to_txt
from team_handler import team_to_csv, team_handler # for testing
filename = os.path.basename(local_file_path)

print("Initalizing ('ism): ")
initalize = False
if initalize is True:
	write_all_teams()
	pokemon_to_txt(filename)# This file will run every command in subsequent order:e
	# commment this one out to test ofc
	#team_handler("https://pokepast.es/b2c2fd8b0038c814", str(0))

team_to_csv(local_teamjson_path)



# team w/ ev's (my team):https://pokepast.es/46e426ed62136f59