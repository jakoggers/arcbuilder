import os
from config import file_path
from team_to_txt import write_all_teams, pokemon_to_txt

filename = os.path.basename(file_path)

print("Initalizing: ")
write_all_teams()
pokemon_to_txt(filename)# This file will run every command in subsequent order: