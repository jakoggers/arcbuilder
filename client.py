import os
from config import local_file_path, local_teamjson_path
from team_to_txt import write_all_teams, pokemon_to_txt
from team_handler import team_to_csv, team_handler # for testing
filename = os.path.basename(local_file_path)

print("Initalizing ('ism): ")
initalize = False
if initalize is True:
	write_all_teams()
	pokemon_to_txt(filename) # This file will run every command in subsequent order:

	# commment this one out to test ofc
	pass

team_handler("https://pokepast.es/471db5ad6ebfbd9f", str(27))
team_handler("https://pokepast.es/46e426ed62136f59", str(0))

#team_to_csv(local_teamjson_path)



# team w/ ev's (my team):https://pokepast.es/46e426ed62136f59