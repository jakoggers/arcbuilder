import os
from config import local_file_path
from team_to_txt import write_all_teams, pokemon_to_txt
from team_handler import team_handler # for testing
filename = os.path.basename(local_file_path)

print("Initalizing ('ism): ")

# commment this one out to test ofc
#write_all_teams()
#pokemon_to_txt(filename)# This file will run every command in subsequent order:e
team_handler("https://pokepast.es/b2c2fd8b0038c814", str(0))
# team w/ ev's (my team):https://pokepast.es/46e426ed62136f59