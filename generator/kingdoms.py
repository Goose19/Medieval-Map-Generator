import random

from models.kingdom import Kingdom

kingdom_prefixes = [
	"Seth", "Eldren", "Valen", "Nord", "Aster",
	"Raven", "Iron", "Silver", "Dawn", "Storm"
]

kingdom_suffixes = [
	"Kingdom", "Realm", "Dominion", "March",
	"Principality", "Crownland"
]

state_types = [
	"kingdom", "duchy", "empire", "republic", "free_city"
]

def choose_state_type(capital, world):
	score = capital["score"]

	if score >= 80 and world.width * world.height >= 2400:
		return "empire"
	
	if score >= 65:
		return random.choice(["kingdom", "republic"])

	if score >= 45:
		return random.choice(["duchy", "kingdom"])
	
	if len(world.cities) <= 4:
		return "free_city"
	
	return random.choice(["duchy", "free_city"])

# state_types = [
# 	"kingdom", "empire", "republic", "principality",
# 	"duchy", "confederation"
# ]

def generate_kingdom_name(state_type):
	prefix = random.choice(kingdom_prefixes)

	suffixes_by_type = {
		"kingdom": ["Kingdom", "Realm", "Crownland"],
		"duchy": ["Duchy", "March", "Principality"],
		"republic": ["Republic", "League", "Commonwealth"],
		"empire": ["Empire", "Imperium"],
		"free_city": ["Free City", "City-State"]
	}

	suffix = random.choice(suffixes_by_type.get(state_type, ["State"]))

	return f"{prefix} {suffix}"

# def generate_kingdom_name():
# 	prefix = random.choice(kingdom_prefixes)
# 	suffix = random.choice(kingdom_suffixes)

# 	return prefix + " " + suffix

def distance(a, b):
	ax, ay = a
	bx, by = b

	return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

def generate_kingdoms(world, count=3):
	random.seed(world.seed + 4000)

	if not world.cities:
		return world

	available_cities = world.cities[:]
	available_cities.sort(key=lambda city: city["score"], reverse=True)

	capitals = []

	capitals.append(available_cities[0])

	while len(capitals) < count and len(capitals) < len(available_cities):
		best_city = None
		best_distance = -1

		for city in available_cities:
			if city in capitals:
				continue

			nearest_capital_distance = None

			for capital in capitals:
				d = distance (
					(city["x"], city["y"]),
					(capital["x"], capital["y"])
				)

				if nearest_capital_distance is None or d < nearest_capital_distance:
					nearest_capital_distance = d

			if nearest_capital_distance > best_distance:
				best_distance = nearest_capital_distance
				best_city = city

		if best_city is None:
			break

		capitals.append(best_city)

	# min_capital_distance = max(8, world.width // 6)

	# for city in available_cities:
	# 	if len(capitals) >= count:
	# 		break

	# 	tooclose = False

	# 	for capital in capitals:
	# 		if distance((city["x"], city["y"]), (capital["x"], capital["y"])) < min_capital_distance:
	# 			tooclose = True
	# 			break

	# 	if tooclose:
	# 		continue

	# 	capitals.append(city)

	for capital in capitals:
		state_type = choose_state_type(capital, world)

		kingdom = Kingdom(
			name = generate_kingdom_name(state_type),
			capital = capital,
			state_type = state_type
			)

		kingdom.cities.append(capital)
		world.kingdoms.append(kingdom)

	for city in world.cities:
		nearest_kingdom = None
		nearest_distance = None

		for kingdom in world.kingdoms:
			capital = kingdom.capital

			d = distance(
				(city["x"], city["y"]),
				(capital["x"], capital["y"])
				)

			if nearest_distance is None or d < nearest_distance:
				nearest_distance = d
				nearest_kingdom = kingdom

		if nearest_kingdom is not None and city not in nearest_kingdom.cities:
			nearest_kingdom.cities.append(city)

	assign_territories(world)

	return world

def assign_territories(world):
	for kingdom in world.kingdoms:
		kingdom.territory = []

	for y in range(world.height):
		for x in range(world.width):
			tile = world.tiles[y][x]

			if tile.biome in ["water", "river"]:
				continue

			nearest_kingdom = None
			nearest_distance = None

			for kingdom in world.kingdoms:
				capital = kingdom.capital

				d = distance(
					(x, y),
					(capital["x"], capital["y"])
				)

				if nearest_distance is None or d < nearest_distance:
					nearest_distance = d
					nearest_kingdom = kingdom

			if nearest_kingdom is not None:
				nearest_kingdom.territory.append((x, y))