from collections import deque

from generator.names import NameGenerator
from models.water_body import WaterBody


CARDINAL_DIRECTIONS = [
	(-1, 0),
	(1, 0),
	(0, -1),
	(0, 1)
]

ALL_DIRECTIONS = [
	(-1, -1), (0, -1), (1, -1),
	(-1, 0),            (1, 0),
	(-1, 1),  (0, 1),   (1, 1)
]

CLIMATE_ZONES = [
	(0.20, "polar"),
	(0.36, "subpolar"),
	(0.58, "temperate"),
	(0.76, "subtropical"),
	(1.01, "tropical")
]


def is_inside(world, x, y):
	return 0 <= x < world.width and 0 <= y < world.height


def is_base_water(tile):
	return tile.biome in ["water", "deep_water"]


def get_cardinal_neighbors(world, x, y):
	for dx, dy in CARDINAL_DIRECTIONS:
		nx = x + dx
		ny = y + dy

		if is_inside(world, nx, ny):
			yield nx, ny


def get_all_neighbors(world, x, y):
	for dx, dy in ALL_DIRECTIONS:
		nx = x + dx
		ny = y + dy

		if is_inside(world, nx, ny):
			yield nx, ny


def collect_water_component(world, start_x, start_y, visited):
	queue = deque([(start_x, start_y)])
	visited.add((start_x, start_y))

	territory = []
	touches_edge = False

	while queue:
		x, y = queue.popleft()
		territory.append((x, y))

		if x == 0 or y == 0 or x == world.width - 1 or y == world.height - 1:
			touches_edge = True

		for nx, ny in get_cardinal_neighbors(world, x, y):
			if (nx, ny) in visited:
				continue

			if not is_base_water(world.tiles[ny][nx]):
				continue

			visited.add((nx, ny))
			queue.append((nx, ny))

	return territory, touches_edge

def create_primary_water_bodies(world, name_generator):
	visited = set()
	components = []

	for y in range(world.height):
		for x in range(world.width):
			if (x, y) in visited:
				continue

			tile = world.tiles[y][x]

			if not is_base_water(tile):
				continue

			territory, touches_edge = collect_water_component(world, x, y, visited)

			components.append({
				"territory": territory,
				"touches_edge": touches_edge
			})

	if not components:
		return

	map_area = world.width * world.height

	sea_area_threshold = max(24, int(map_area * 0.05))
	coastal_sea_threshold = max(12, int(map_area * 0.01))

	sea_number = 1
	lake_number = 1

	for component in components:
		territory = component["territory"]
		touches_edge = component["touches_edge"]

		area = len(territory)

		is_sea = False

		if area >= sea_area_threshold:
			is_sea = True
		elif touches_edge and area >= coastal_sea_threshold:
			is_sea = True

		if is_sea:
			water_body = WaterBody(
				f"sea_{sea_number}",
				name_generator.generate_sea_name(),
				"sea",
				territory
			)

			world.seas.append(water_body)
			sea_number += 1

		else:
			water_body = WaterBody(
				f"lake_{lake_number}",
				name_generator.generate_lake_name(),
				"lake",
				territory
			)

			world.lakes.append(water_body)
			lake_number += 1

		world.water_bodies.append(water_body)

		for water_x, water_y in territory:
			world.tiles[water_y][water_x].water_body_id = water_body.id

def has_land_in_direction(world, x, y, dx, dy, radius=3):
	for distance in range(1, radius + 1):
		nx = x + dx * distance
		ny = y + dy * distance

		if not is_inside(world, nx, ny):
			return False

		if not is_base_water(world.tiles[ny][nx]):
			return True

	return False


def get_land_direction_count(world, x, y, radius=3):
	count = 0

	for dx, dy in CARDINAL_DIRECTIONS:
		if has_land_in_direction(world, x, y, dx, dy, radius):
			count += 1

	return count


def is_bay_seed(world, x, y, radius=3):
	if x == 0 or y == 0 or x == world.width - 1 or y == world.height - 1:
		return False

	land_left = has_land_in_direction(world, x, y, -1, 0, radius)
	land_right = has_land_in_direction(world, x, y, 1, 0, radius)
	land_up = has_land_in_direction(world, x, y, 0, -1, radius)
	land_down = has_land_in_direction(world, x, y, 0, 1, radius)

	if land_left and land_right:
		return True

	if land_up and land_down:
		return True

	return False


def collect_bay_seed_component(world, start, candidates, visited):
	queue = deque([start])
	visited.add(start)

	component = []

	while queue:
		x, y = queue.popleft()
		component.append((x, y))

		for nx, ny in get_all_neighbors(world, x, y):
			position = (nx, ny)

			if position in visited:
				continue

			if position not in candidates:
				continue

			visited.add(position)
			queue.append(position)

	return component


def expand_bay_territory(world, sea, component, depth=2):
	sea_tiles = set(sea.territory)

	territory = set(component)
	frontier = set(component)

	for _ in range(depth):
		next_frontier = set()

		for x, y in frontier:
			for nx, ny in get_cardinal_neighbors(world, x, y):
				position = (nx, ny)

				if position in territory:
					continue

				if position not in sea_tiles:
					continue

				if get_land_direction_count(world, nx, ny) < 2:
					continue

				territory.add(position)
				next_frontier.add(position)

		frontier = next_frontier

		if not frontier:
			break

	return sorted(territory)


def create_bays(world, name_generator):
	bay_number = 1
	occupied_bay_tiles = set()

	for sea in world.seas:
		if sea.area < 20:
			continue

		candidates = set()

		for x, y in sea.territory:
			if is_bay_seed(world, x, y):
				candidates.add((x, y))

		visited = set()

		for start in sorted(candidates):
			if start in visited:
				continue

			component = collect_bay_seed_component(world, start, candidates, visited)
			territory = expand_bay_territory(world, sea, component)

			if len(territory) < 2:
				continue

			max_bay_area = max(12, int(sea.area * 0.20))

			if len(territory) > max_bay_area:
				continue

			if any(position in occupied_bay_tiles for position in territory):
				continue

			bay = WaterBody(
				f"bay_{bay_number}",
				name_generator.generate_bay_name(),
				"bay",
				territory,
				parent_id=sea.id
			)

			world.water_bodies.append(bay)
			world.bays.append(bay)

			for bay_x, bay_y in territory:
				world.tiles[bay_y][bay_x].bay_id = bay.id
				occupied_bay_tiles.add((bay_x, bay_y))

			bay_number += 1


def resolve_climate_zone(temperature):
	for max_temperature, climate_zone in CLIMATE_ZONES:
		if temperature < max_temperature:
			return climate_zone

	return "tropical"


def generate_climate_zones(world):
	for row in world.tiles:
		for tile in row:
			tile.climate_zone = resolve_climate_zone(tile.temperature)


def generate_geography(world):
	name_generator = NameGenerator(world.seed)

	world.water_bodies = []
	world.seas = []
	world.lakes = []
	world.bays = []

	for row in world.tiles:
		for tile in row:
			tile.water_body_id = None
			tile.bay_id = None

	create_primary_water_bodies(world, name_generator)
	create_bays(world, name_generator)
	generate_climate_zones(world)

	return world