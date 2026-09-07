import random


CITY_PREFIXES = [
	"North", "South", "East", "West",
	"Stone", "River", "High", "Old",
	"Red", "White", "Iron", "Green",
	"Black", "Grey", "Gold", "Ash",
	"Oak", "Wolf", "Raven", "Storm"
]

CITY_SUFFIXES = [
	"ford", "helm", "hold", "wick",
	"bridge", "fall", "watch", "keep",
	"ton", "burg", "haven", "rest",
	"mouth", "field", "wall", "gate",
	"wood", "hill", "rock", "dale"
]


STATE_ROOTS = [
	"Seth", "Eldren", "Valen", "Nord",
	"Aster", "Raven", "Iron", "Silver",
	"Dawn", "Storm", "Arden", "Varen",
	"Thalen", "Eiren", "Maren", "Draven",
	"Corven", "Aldren", "Veyr", "Taren"
]


STATE_SUFFIXES = {
	"kingdom": [
		"Kingdom",
		"Realm",
		"Crownland"
	],

	"duchy": [
		"Duchy",
		"March",
		"Principality"
	],

	"republic": [
		"Republic",
		"League",
		"Commonwealth"
	],

	"empire": [
		"Empire",
		"Imperium"
	],

	"free_city": [
		"Free City",
		"City-State"
	]
}


RIVER_PREFIXES = [
	"Silver", "Black", "White", "Red",
	"Green", "Grey", "Cold", "Deep",
	"Swift", "Long", "High", "Dark",
	"Bright", "Clear", "Old", "Blue"
]

RIVER_SUFFIXES = [
	"water",
	"flow",
	"stream",
	"run",
	"wash",
	"river"
]


LAKE_PREFIXES = [
	"Silver", "Crystal", "Black", "White",
	"Deep", "Cold", "Clear", "Blue",
	"Silent", "Mirror", "Moon", "Star"
]

LAKE_SUFFIXES = [
	"Lake",
	"Water",
	"Mere"
]

SEA_PREFIXES = [
	"Azure", "Silver", "Grey", "Black",
	"White", "Emerald", "Storm", "Cold",
	"Shattered", "Silent", "Sapphire", "Iron"
]

SEA_SUFFIXES = [
	"Sea",
	"Waters",
	"Expanse"
]


BAY_PREFIXES = [
	"Silver", "Black", "White", "Red",
	"Green", "Grey", "Storm", "Wolf",
	"Raven", "Moon", "King", "Deep"
]

BAY_SUFFIXES = [
	"Bay",
	"Gulf",
	"Bight"
]

MOUNTAIN_PREFIXES = [
	"Stone", "Iron", "Black", "White",
	"High", "Grey", "Red", "Frost",
	"Storm", "Dragon", "Wolf", "Ash"
]

MOUNTAIN_SUFFIXES = [
	"Peak",
	"Mount",
	"Horn",
	"Spire",
	"Crown",
	"Fang"
]


REGION_PREFIXES = [
	"North", "South", "East", "West",
	"High", "Low", "Green", "Black",
	"Old", "New", "Outer", "Inner"
]

REGION_SUFFIXES = [
	"lands",
	"march",
	"reach",
	"vale",
	"fields",
	"wood",
	"coast",
	"heights"
]

PROVINCE_PREFIXES = [
	"North", "South", "East", "West",
	"Upper", "Lower", "Old", "High",
	"Green", "Grey", "Black", "White",
	"River", "Stone", "Iron", "Oak"
]

PROVINCE_SUFFIXES = [
	"march",
	"shire",
	"vale",
	"field",
	"wood",
	"land",
	"dale",
	"reach"
]


class NameGenerator:
	def __init__(self, seed):
		self.city_rng = random.Random(seed + 10000)
		self.state_rng = random.Random(seed + 11000)
		self.river_rng = random.Random(seed + 12000)
		self.lake_rng = random.Random(seed + 13000)
		self.mountain_rng = random.Random(seed + 14000)
		self.region_rng = random.Random(seed + 15000)
		self.province_rng = random.Random(seed + 16000)
		self.sea_rng = random.Random(seed + 17000)
		self.bay_rng = random.Random(seed + 18000)

		self.used_city_names = set()
		self.used_state_names = set()
		self.used_river_names = set()
		self.used_lake_names = set()
		self.used_mountain_names = set()
		self.used_region_names = set()
		self.used_province_names = set()
		self.used_sea_names = set()
		self.used_bay_names = set()


	def generate_unique_name(self, create_name, used_names, attempts=100):
		for _ in range(attempts):
			name = create_name()

			if name not in used_names:
				used_names.add(name)
				return name

		raise RuntimeError("Unable to generate a unique name")

	def generate_city_name(self):
		def create_name():
			prefix = self.city_rng.choice(CITY_PREFIXES)
			suffix = self.city_rng.choice(CITY_SUFFIXES)
			return prefix + suffix

		return self.generate_unique_name(create_name, self.used_city_names)

	def generate_state_name(self, state_type):
		def create_name():
			root = self.state_rng.choice(STATE_ROOTS)

			if state_type in STATE_SUFFIXES:
				suffixes = STATE_SUFFIXES[state_type]
			else:
				suffixes = ["State"]

			suffix = self.state_rng.choice(suffixes)
			return f"{root} {suffix}"

		return self.generate_unique_name(create_name, self.used_state_names)

	def generate_river_name(self):
		def create_name():
			prefix = self.river_rng.choice(RIVER_PREFIXES)
			suffix = self.river_rng.choice(RIVER_SUFFIXES)

			if suffix == "river":
				return f"{prefix} River"

			return prefix + suffix

		return self.generate_unique_name(create_name, self.used_river_names)

	def generate_lake_name(self):
		def create_name():
			prefix = self.lake_rng.choice(LAKE_PREFIXES)
			suffix = self.lake_rng.choice(LAKE_SUFFIXES)
			return f"{prefix} {suffix}"

		return self.generate_unique_name(create_name, self.used_lake_names)

	def generate_mountain_name(self):
		def create_name():
			prefix = self.mountain_rng.choice(MOUNTAIN_PREFIXES)
			suffix = self.mountain_rng.choice(MOUNTAIN_SUFFIXES)
			return f"{prefix} {suffix}"

		return self.generate_unique_name(create_name, self.used_mountain_names)

	def generate_province_name(self):
		def create_name():
			prefix = self.province_rng.choice(PROVINCE_PREFIXES)
			suffix = self.province_rng.choice(PROVINCE_SUFFIXES)
			return prefix + suffix

		return self.generate_unique_name(create_name, self.used_province_names)

	def generate_region_name(self):
		def create_name():
			prefix = self.region_rng.choice(REGION_PREFIXES)
			suffix = self.region_rng.choice(REGION_SUFFIXES)
			return prefix + suffix

		return self.generate_unique_name(create_name, self.used_region_names)

	def generate_sea_name(self):
		def create_name():
			prefix = self.sea_rng.choice(SEA_PREFIXES)
			suffix = self.sea_rng.choice(SEA_SUFFIXES)
			return f"{prefix} {suffix}"

		return self.generate_unique_name(create_name, self.used_sea_names)

	def generate_bay_name(self):
		def create_name():
			prefix = self.bay_rng.choice(BAY_PREFIXES)
			suffix = self.bay_rng.choice(BAY_SUFFIXES)
			return f"{prefix} {suffix}"

		return self.generate_unique_name(create_name, self.used_bay_names)