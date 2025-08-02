import os
from config import local_file_path, local_teamjson_path
from team_to_txt import write_all_teams, pokemon_to_txt
from team_handler import team_to_csv, team_handler # for testing
import time
filename = os.path.basename(local_file_path)


initalize = input("Write all teams to JSON, TXT, and to CSV? (Y or N) ")
print("Initalizing ('ism): ")
begin = str(initalize).capitalize()
if begin == "Y":

	wat_time = time.time()
	write_all_teams()
	print(f"Completed Write Time in {time.time() - wat_time}")

	pkmntxt_time = time.time()
	pokemon_to_txt(filename) # This file will run every command in subsequent order:
	print(f"Completed Write Time in {(time.time() - pkmntxt_time) / 60} Minutes")

	csv_time = time.time()
	team_to_csv(local_teamjson_path)
	print(f"Completed Write Time in {time.time() - csv_time}")

	# commment this one out to test ofc
elif begin == "A":
	which_team = input("Give me a team to test with: ")
	team_handler(which_team, str(0))
	print(f"Test team in file: 0")
elif begin == "C":
	team_to_csv(local_teamjson_path)
	print("Instant CSV!")
else:
	print("It had no effect!")
# team_handler("https://pokepast.es/46e426ed62136f59", str(0))
#team_handler("https://pokepast.es/41a3259337c0ca59", str(71))


# Test Teams:
"""
	https://pokepast.es/46e426ed62136f59 // made by hsxd_snakob himself WITH IVS/EVS/NATURE
	https://pokepast.es/ae4ac698461d3b7a // made by hsxd_snakob himself WITHOUT IVS/EVS/NATURE
	https://pokepast.es/ef6920d4f30db897 // made by idk
	https://pokepast.es/722a7a53b4f46592 - made by
	https://pokepast.es/84c0b7c14de37a87 // portland champion team, scarvi regulation I: centered around Kyogre
	https://pokepast.es/8a2335a101620d91 // team around ho-oh
	https://pokepast.es/5ee3277dc45acb8c // team around zamazenta
	https://pokepast.es/61a6451d1fb10777 // parse breaker
	https://pokepast.es/d4061070550b4255 // parse breaker v2
"""
