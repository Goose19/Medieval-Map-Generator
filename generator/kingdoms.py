# It's a new version of the kingdoms.py
import random

from models.kingdom import Kingdom
from generator.cities import is_near_water
from generator.names import NameGenerator


# kingdom_prefixes = [
# 	"Seth", "Eldren", "Valen", "Nord", "Aster",
# 	"Raven", "Iron", "Silver", "Dawn", "Storm"
# ]

state_types = [
	"kingdom",
	"duchy",
	"empire",
	"republic",
	"free_city"
]


CULTURES = {
	"lowland": {
		"biomes": {
			"plains": 5,
			"dry_plains": 2,
			"forest": 1
		},
		"state_weights": {
			"kingdom": 5,
			"duchy": 2,
			"republic": 3,
			"empire": 2,
			"free_city": 1
		}
	},

	"woodland": {
		"biomes": {
			"forest": 5,
			"taiga": 2,
			"plains": 2
		},
		"state_weights": {
			"kingdom": 4,
			"duchy": 4,
			"republic": 2,
			"empire": 1,
			"free_city": 1
		}
	},

	"northern": {
		"biomes": {
			"taiga": 5,
			"tundra": 5,
			"mountain": 1
		},
		"state_weights": {
			"kingdom": 5,
			"duchy": 4,
			"republic": 1,
			"empire": 2,
			"free_city": 1
		}
	},

	"highland": {
		"biomes": {
			"mountain": 6,
			"taiga": 2,
			"dry_plains": 1
		},
		"state_weights": {
			"kingdom": 3,
			"duchy": 6,
			"republic": 1,
			"empire": 2,
			"free_city": 1
		}
	},

	"steppe": {
		"biomes": {
			"dry_plains": 6,
			"plains": 2,
			"desert": 2
		},
		"state_weights": {
			"kingdom": 4,
			"duchy": 3,
			"republic": 1,
			"empire": 4,
			"free_city": 1
		}
	},

	"southern": {
		"biomes": {
			"desert": 5,
			"jungle": 5,
			"plains": 1
		},
		"state_weights": {
			"kingdom": 3,
			"duchy": 1,
			"republic": 3,
			"empire": 4,
			"free_city": 2
		}
	},

	"maritime": {
		"biomes": {},
		"state_weights": {
			"kingdom": 2,
			"duchy": 1,
			"republic": 6,
			"empire": 2,
			"free_city": 5
		}
	}
}


def distance(a, b):
	ax, ay = a
	bx, by = b

	return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5


def get_capital_environment(world, capital, radius=4):
	biome_counts = {}

	water_tiles = 0
	total_tiles = 0

	for dy in range(-radius, radius + 1):
		for dx in range(-radius, radius + 1):
			x = capital["x"] + dx
			y = capital["y"] + dy

			if not (0 <= x < world.width and 0 <= y < world.height):
				continue

			tile = world.tiles[y][x]
			biome = tile.biome

			if biome == "city":
				biome = capital.get("biome", "plains")

			total_tiles += 1

			if biome in ["water", "river"]:
				water_tiles += 1
				continue

			biome_counts[biome] = (biome_counts.get(biome, 0) + 1)

	water_ratio = water_tiles / max(1, total_tiles)

	return biome_counts, water_ratio


def choose_culture(world, capital):
	biome_counts, water_ratio = (get_capital_environment(world, capital))

	culture_scores = {}

	for culture_name, culture_data in CULTURES.items():
		if culture_name == "maritime":
			continue

		score = 0.0

		for biome, count in biome_counts.items():
			biome_weight = (culture_data["biomes"].get(biome, 0))

			score += count * biome_weight

		score += random.random() * 2.0

		culture_scores[culture_name] = score

	if water_ratio >= 0.22:
		culture_scores["maritime"] = (water_ratio * 180.0 + random.random() * 2.0)

	else:
		culture_scores["maritime"] = 0.0

	return max(culture_scores, key=culture_scores.get)


def weighted_choice(weights):

	items = []

	for item, weight in weights.items():
		if weight <= 0:
			continue

		items.extend([item] * int(weight))

	if not items:
		return "kingdom"

	return random.choice(items)


def choose_state_type(capital, world, culture):

	score = capital["score"]

	weights = (CULTURES[culture]["state_weights"].copy())

	# if (score < 70 or world.width * world.height < 1800):
	# 	weights["empire"] = 0

	# elif (score >= 80 and world.width * world.height >= 2400):
	# 	weights["empire"] *= 3

	if (score < 11 or world.width * world.height < 1800):
		weights["empire"] = 0

	elif (score >= 13 and world.width * world.height >= 2400):
		weights["empire"] *= 3

	if len(world.cities) <= 4:
		weights["free_city"] *= 3

	return weighted_choice(weights)


# def generate_kingdom_name(state_type):
# 	prefix = random.choice(kingdom_prefixes)

# 	suffixes_by_type = {
# 		"kingdom": [
# 			"Kingdom",
# 			"Realm",
# 			"Crownland"
# 		],

# 		"duchy": [
# 			"Duchy",
# 			"March",
# 			"Principality"
# 		],

# 		"republic": [
# 			"Republic",
# 			"League",
# 			"Commonwealth"
# 		],

# 		"empire": [
# 			"Empire",
# 			"Imperium"
# 		],

# 		"free_city": [
# 			"Free City",
# 			"City-State"
# 		]
# 	}

# 	suffix = random.choice(suffixes_by_type.get(state_type, ["State"]))

# 	return f"{prefix} {suffix}"

def get_cluster_center(cities):
	center_x = sum(city["x"] for city in cities) / len(cities)
	center_y = sum(city["y"] for city in cities) / len(cities)

	return center_x, center_y


def choose_initial_cluster_centers(cities, count):
	count = min(count, len(cities))

	first_city = max(cities, key=lambda city: city["score"])
	centers = [(first_city["x"], first_city["y"])]

	while len(centers) < count:
		best_city = None
		best_value = -1

		for city in cities:
			position = (city["x"], city["y"])

			if position in centers:
				continue

			min_distance = min(distance(position, center) for center in centers)
			value = min_distance + city["score"] * 0.35

			if value > best_value:
				best_value = value
				best_city = city

		if best_city is None:
			break

		centers.append((best_city["x"], best_city["y"]))

	return centers


def cluster_cities(cities, count, iterations=12):
	if not cities:
		return []

	centers = choose_initial_cluster_centers(cities, count)

	for _ in range(iterations):
		clusters = [[] for _ in centers]

		for city in cities:
			position = (city["x"], city["y"])
			nearest_index = min(range(len(centers)), key=lambda i: distance(position, centers[i]))
			clusters[nearest_index].append(city)

		new_centers = []

		for index, cluster in enumerate(clusters):
			if cluster:
				new_centers.append(get_cluster_center(cluster))
			else:
				new_centers.append(centers[index])

		if all(distance(centers[i], new_centers[i]) < 0.01 for i in range(len(centers))):
			break

		centers = new_centers

	return [cluster for cluster in clusters if cluster]


def get_capital_score(world, city, cluster):
	score = city.get("score", 0) * 10.0

	center_x, center_y = get_cluster_center(cluster)
	distance_from_cluster_center = distance((city["x"], city["y"]), (center_x, center_y))

	score -= distance_from_cluster_center * 2.0

	if is_near_water(world, city["x"], city["y"], radius=3):
		score += 12.0

	if len(cluster) > 1:
		average_distance = sum(distance((city["x"], city["y"]), (other["x"], other["y"])) for other in cluster if other is not city) / (len(cluster) - 1)
		score -= average_distance * 0.5

	edge_distance = min(city["x"], city["y"], world.width - 1 - city["x"], world.height - 1 - city["y"])
	score += min(edge_distance, 10) * 0.5

	return score


def choose_capital(world, cluster):
	return max(cluster, key=lambda city: get_capital_score(world, city, cluster))

def generate_kingdoms(world, count=3):
	random.seed(world.seed + 4000)
	name_generator = NameGenerator(world.seed)

	if not world.cities:
		return world

	world.kingdoms = []

	clusters = cluster_cities(world.cities, count)

	kingdom_number = 1

	for cluster in clusters:
		capital = choose_capital(world, cluster)
		culture = choose_culture(world, capital)
		state_type = choose_state_type(capital, world, culture)

		kingdom_id = "kingdom_" + str(kingdom_number)

		kingdom = Kingdom(
			kingdom_id = kingdom_id,
			name=name_generator.generate_state_name(state_type),
			capital=capital,
			state_type=state_type,
			culture=culture
		)

		kingdom.cities = list(cluster)
		world.kingdoms.append(kingdom)

		kingdom_number += 1

	assign_territories(world)
	determine_neighbors(world)

	return world


def assign_territories(world):
	for kingdom in world.kingdoms:
		kingdom.territory = []

	for y in range(world.height):
		for x in range(world.width):
			tile = world.tiles[y][x]

			if tile.biome in ["water", "deep_water"]:
				continue

			nearest_kingdom = None
			nearest_distance = None

			for kingdom in world.kingdoms:
				capital = kingdom.capital

				d = distance((x, y), (capital["x"], capital["y"]))

				if (nearest_distance is None or d < nearest_distance):
					nearest_distance = d
					nearest_kingdom = kingdom

			if nearest_kingdom is not None:
				nearest_kingdom.territory.append((x, y))
				tile.kingdom_id = nearest_kingdom.id

def determine_neighbors(world):
	territory_owner = {}

	for kingdom in world.kingdoms:
		kingdom.neighbors = []
		kingdom.border_lengths = {}

		for x, y in kingdom.territory:
			territory_owner[(x, y)] = kingdom

	directions = [
		(1, 0),
		(0, 1)
	]

	for y in range(world.height):
		for x in range(world.width):
			current_kingdom = territory_owner.get((x, y))

			if current_kingdom is None:
				continue

			for dx, dy in directions:
				nx = x + dx
				ny = y + dy

				if nx < 0 or ny < 0:
					continue

				if nx >= world.width or ny >= world.height:
					continue

				neighbor_kingdom = territory_owner.get((nx, ny))

				if neighbor_kingdom is None:
					continue

				if neighbor_kingdom is current_kingdom:
					continue

				if neighbor_kingdom not in current_kingdom.neighbors:
					current_kingdom.neighbors.append(neighbor_kingdom)

				if current_kingdom not in neighbor_kingdom.neighbors:
					neighbor_kingdom.neighbors.append(current_kingdom)

				if neighbor_kingdom.name not in current_kingdom.border_lengths:
					current_kingdom.border_lengths[neighbor_kingdom.name] = 0

				if current_kingdom.name not in neighbor_kingdom.border_lengths:
					neighbor_kingdom.border_lengths[current_kingdom.name] = 0

				current_kingdom.border_lengths[neighbor_kingdom.name] += 1
				neighbor_kingdom.border_lengths[current_kingdom.name] += 1

	return world

def detect_political_borders(world):
	for row in world.tiles:
		for tile in row:
			tile.region_border = False
			tile.kingdom_border = False
	
	directions = [
		(-1, 0),
		(1, 0),
		(0, -1),
		(0, 1),
	]

	for y in range(world.height):
		for x in range(world.width):
			tile = world.tiles[y][x]

			if tile.kingdom_id is None:
				continue
			
			for direction in directions:
				dx = direction[0]
				dy = direction[1]

				nx = x + dx
				ny = y + dy

				if nx < 0:
					continue
				
				if ny < 0:
					continue
				
				if nx >= world.width:
					continue

				if ny >= world.height:
					continue
				
				neighbor_tile = world.tiles[ny][nx]

				if tile.kingdom_id != neighbor_tile.kingdom_id:
					tile.kingdom_border = True
					continue
				
				if tile.region_id != neighbor_tile.region_id:
					tile.region_border = True
					