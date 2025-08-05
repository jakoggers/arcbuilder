import pandas as pd

pokemon_csv = pd.read_csv("csv_files/mapped_team_data.csv")

ev_sum = 0
for i in range(4, 10):
    pokemon_ev = pokemon_csv.iloc[0, i]
    ev_sum += pokemon_ev if pokemon_ev > 0 else 0

fragmented = True if ev_sum == 0 else False

name_modifications = {
	"gastrodon-east": "gastrodon",
	"gastrodon-west": "gastrodon",
	"indeedee-f": "indeedee-female",
	"necrozma-dusk-mane": "necrozma-dusk",
	"necrozma-dawn-wings": "necrozma-dawn",
	"ogerpon-wellspring": "ogerpon-wellspring",
	"ogerpon-hearthflame": "ogerpon-hearthflame",
	"ogerpon-cornerstone": "ogerpon-cornerstone-mask",
	"sinistcha-masterpiece": "sinistcha"
}

name = "gastrodon-east"
print("Original Name: ", name)
if name in name_modifications:
	name = name_modifications[name]

print("New name: ", name)


if fragmented:
    pass
    # rank base stat total of pokemon
