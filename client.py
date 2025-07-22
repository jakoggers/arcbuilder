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
	team_to_csv(local_teamjson_path)
	# commment this one out to test ofc
	pass
team_handler("https://pokepast.es/46e426ed62136f59", str(0))
#team_handler("https://pokepast.es/41a3259337c0ca59", str(71))

# team w/ ev's (my team):https://pokepast.es/46e426ed62136f59

# Test Teams:
"""
	https://pokepast.es/46e426ed62136f59 // made by hsxd_snakob himself
	https://pokepast.es/ef6920d4f30db897 // made by idk
	https://pokepast.es/722a7a53b4f46592 - made by
	https://pokepast.es/84c0b7c14de37a87 // portland champion team, scarvi regulation I: centered around Kyogre
	https://pokepast.es/8a2335a101620d91 // team around ho-oh
	https://pokepast.es/5ee3277dc45acb8c // team around zamazenta
	https://pokepast.es/61a6451d1fb10777 // parse breaker
"""
