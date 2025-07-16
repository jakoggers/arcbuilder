import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

from config import local_teamjson_path

data_read = pd.read_csv("Full Team Data.csv")
# Reduntant, but makes it easier to read
data_read.rename(columns={
	'name': 'Name',
	'item': 'Item',
	'gender': 'Gender',
	'ability': 'Ability',
	'level': 'Level',
	'tera_type': "Tera Type",
	'nature': 'Nature',
	'evs.ev_hp': 'HP EV',
	'evs.ev_attack': 'Attack EV',
	'evs.ev_defense': 'Defense EV',
	'evs.ev_special_attack': 'Special Attack EV',
	'evs.ev_special_defense': 'Special Defense EV',
	'evs.ev_speed': 'Speed EV',
	'ivs.iv_hp': 'HP IV',
	'ivs.iv_attack': 'Attack IV',
	'ivs.iv_defense': 'Defense IV',
	'ivs.iv_special_attack': 'Special Attack IV',
	'ivs.iv_special_defense': 'Special Defense IV',
	'ivs.iv_speed': 'Speed IV',
	'moves.move_1': 'Move 1',
	'moves.move_2': 'Move 2',
	'moves.move_3': 'Move 3',
	'moves.move_4': 'Move 4',
	}, inplace=True)


print(data_read.shape)
print(data_read.columns)
