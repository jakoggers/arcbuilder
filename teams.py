# all the pokemon in one team

pokemon1 = {
	"name": "",
	"item": "",
	"gender": "",
	"ability": "",
	"level": 50,
	"tera_type": "",
	# separate
	"nature": "",
	# evs
	"evs": {
		"ev_hp": 0,
		"ev_attack": 0,
		"ev_defense": 0,
		"ev_special_attack": 0,
		"ev_special_defense": 0,
		"ev_speed": 0,
	},
	# ivs
	"ivs": {
		"iv_hp": 31,
		"iv_attack": 31,
		"iv_defense": 31,
		"iv_special_attack": 31,
		"iv_special_defense": 31,
		"iv_speed": 31,
	},
	# Moves
	"moves": {"move_1": "", "move_2": "", "move_3": "", "move_4": ""},
}

pokemon2 = {
	"name": "",
	"item": "",
	"gender": "",
	"ability": "",
	"level": 50,
	"tera_type": "",
	# separate
	"nature": "",
	# evs
	"evs": {
		"ev_hp": 0,
		"ev_attack": 0,
		"ev_defense": 0,
		"ev_special_attack": 0,
		"ev_special_defense": 0,
		"ev_speed": 0,
	},
	# ivs
	"ivs": {
		"iv_hp": 31,
		"iv_attack": 31,
		"iv_defense": 31,
		"iv_special_attack": 31,
		"iv_special_defense": 31,
		"iv_speed": 31,
	},
	# Moves
	"moves": {"move_1": "", "move_2": "", "move_3": "", "move_4": ""},
}

pokemon3 = {
	"name": "",
	"item": "",
	"gender": "",
	"ability": "",
	"level": 50,
	"tera_type": "",
	# separate
	"nature": "",
	# evs
	"evs": {
		"ev_hp": 0,
		"ev_attack": 0,
		"ev_defense": 0,
		"ev_special_attack": 0,
		"ev_special_defense": 0,
		"ev_speed": 0,
	},
	# ivs
	"ivs": {
		"iv_hp": 31,
		"iv_attack": 31,
		"iv_defense": 31,
		"iv_special_attack": 31,
		"iv_special_defense": 31,
		"iv_speed": 31,
	},
	# Moves
	"moves": {"move_1": "", "move_2": "", "move_3": "", "move_4": ""},
}

pokemon4 = {
	"name": "",
	"item": "",
	"gender": "",
	"ability": "",
	"level": 50,
	"tera_type": "",
	# separate
	"nature": "",
	# evs
	"evs": {
		"ev_hp": 0,
		"ev_attack": 0,
		"ev_defense": 0,
		"ev_special_attack": 0,
		"ev_special_defense": 0,
		"ev_speed": 0,
	},
	# ivs
	"ivs": {
		"iv_hp": 31,
		"iv_attack": 31,
		"iv_defense": 31,
		"iv_special_attack": 31,
		"iv_special_defense": 31,
		"iv_speed": 31,
	},
	# Moves
	"moves": {"move_1": "", "move_2": "", "move_3": "", "move_4": ""},
}

pokemon5 = {
	"name": "",
	"item": "",
	"gender": "",
	"ability": "",
	"level": 50,
	"tera_type": "",
	# separate
	"nature": "",
	# evs
	"evs": {
		"ev_hp": 0,
		"ev_attack": 0,
		"ev_defense": 0,
		"ev_special_attack": 0,
		"ev_special_defense": 0,
		"ev_speed": 0,
	},
	# ivs
	"ivs": {
		"iv_hp": 31,
		"iv_attack": 31,
		"iv_defense": 31,
		"iv_special_attack": 31,
		"iv_special_defense": 31,
		"iv_speed": 31,
	},
	# Moves
	"moves": {"move_1": "", "move_2": "", "move_3": "", "move_4": ""},
}

pokemon6 = {
	"name": "",
	"item": "",
	"gender": "",
	"ability": "",
	"level": 50,
	"tera_type": "",
	# separate
	"nature": "",
	# evs
	"evs": {
		"ev_hp": 0,
		"ev_attack": 0,
		"ev_defense": 0,
		"ev_special_attack": 0,
		"ev_special_defense": 0,
		"ev_speed": 0,
	},
	# ivs
	"ivs": {
		"iv_hp": 31,
		"iv_attack": 31,
		"iv_defense": 31,
		"iv_special_attack": 31,
		"iv_special_defense": 31,
		"iv_speed": 31,
	},
	# Moves
	"moves": {"move_1": "", "move_2": "", "move_3": "", "move_4": ""},
}

pokemon_team_structure = [pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6]

class PokemonData:
	# evs, ivs, and moves are DICTS
	# , item, gender, ability, level, tera_type, nature, evs, ivs, moves
	name = ""
	item = ""
	ability = ""
	level = 50
	tera_type = ""
	default_gender = ""
	default_nature = ""
	default_evs = {
			"ev_hp": 0,
			"ev_attack": 0,
			"ev_defense": 0,
			"ev_special_attack": 0,
			"ev_special_defense": 0,
			"ev_speed": 0,
		}
	default_ivs = {
			"iv_hp": 31,
			"iv_attack": 31,
			"iv_defense": 31,
			"iv_special_attack": 31,
			"iv_special_defense": 31,
			"iv_speed": 31,
		}
	moves = {}

	def __init__(self, name, item, ability, tera_type, moves, gender = default_gender, nature = default_nature, evs = default_evs, ivs = default_ivs):
		self.name = name
		self.item = item
		self.gender = gender  # set it depending on the pokemon
		self.ability = ability
		self.level = "50"
		self.tera_type = tera_type  # make it the same as the given pokemon
		self.nature = nature  # random
		self.evs = evs
		self.ivs = ivs
		self.moves = moves

	def __str__(self):
		return f"Name: {self.name} \nItem: {self.item} \nAbility: {self.ability} \nTera Type: {self.tera_type} \nMoveset: {self.moves}\nGender: {self.gender} \nNature: {self.nature} \nEVs: {self.evs} \nIVs: {self.ivs} "

"""
take it, turn it into a dictionary?

gallade_evs = {
	"ev_hp": 0,
	"ev_attack": 252,
	"ev_defense": 0,
	"ev_special_attack": 0,
	"ev_special_defense": 4,
	"ev_speed": 252,
}
gallade_ivs = {
	"iv_hp": 31,
	"iv_attack": 31,
	"iv_defense": 31,
	"iv_special_attack": 31,
	"iv_special_defense": 31,
	"iv_speed": 31,
}
gallade_moves = {
	"move_1": "Swords Dance",
	"move_2": "Sacred Sword",
	"move_3": "Psycho Cut",
	"move_4": "Shadow Sneak",
}
gallade = PokemonData(
	"Gallade",
	"Life Orb",
	"Sharpness",
	"Fighting",
	gallade_moves,
	"Male",
	"Adamant",
	gallade_evs,
	gallade_ivs,
)

ogerpon = PokemonData("Ogerpon-Hearthflame", "Hearthflame Mask", "Mold Breaker", "Fire", {"Ivy Cudgel", "Grassy Glide", "Follow Me", "Spiky Shield"})
print(gallade)
print(ogerpon)
"""