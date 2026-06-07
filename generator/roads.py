from heapq import heappush, heappop

biome_cost = {
	"water": 9999,
	"river": 6,
	"bridge": 2,
	"mountain": 14,
	"forest": 5,
	"taiga": 5,
	"tundra": 4,
	"desert": 6,
	"jungle": 8,
	"dry_plains": 2,
	"plains": 1,
	"city": 1,
	"road": 1,
}

def heuristic(a,b):
	ax,ay = a
	bx,by = b
	return abs(ax - bx) + abs(ay - by)

def get_neighbors(world, x, y):
	directions = [
		(1, 0),
		(-1, 0),
		(0, 1),
		(0, -1),
	]

	for dx, dy in directions:
		nx = x + dx
		ny = y + dy

		if 0 <= nx < world.width and 0 <= ny < world.height:
			yield nx, ny

def get_tile_cost(tile):
	return biome_cost.get(tile.biome, 3)

def find_path(world, start, goal):
	frontier = []
	heappush(frontier, (0, start))

	camefrom = {start: None}
	toofar = {start: 0}

	while frontier:
		_, i = heappop(frontier)

		if i == goal:
			break

		x, y = i

		for nx, ny in get_neighbors(world, x, y):
			next_tile = world.tiles[ny][nx]
			tilecost = get_tile_cost(next_tile)

			if tilecost >= 9999:
				continue

			newcost = toofar[i] + tilecost
			nextpos = (nx, ny)

			if nextpos not in toofar or newcost < toofar[nextpos]:
				toofar[nextpos] = newcost
				prior = newcost + heuristic(nextpos, goal)
				heappush(frontier, (prior, nextpos))
				camefrom[nextpos] = i

	if goal not in camefrom:
		return []

	path = []
	i = goal

	while i is not None:
		path.append(i)
		i = camefrom[i]

	path.reverse()
	return path

def mark_road(world, path):
	for x, y in path:
		tile = world.tiles[y][x]

		if tile.biome in ["city", "water"]:
			continue

		if tile.biome == "river":
			tile.biome = "bridge"
			continue

		tile.biome = "road"


def connect_cities_with_roads(world, connections_per_city=2):
	if len(world.cities) < 2:
		return world

	citypoints = [(city["x"], city["y"]) for city in world.cities]
	road_pairs = set()

	for city in citypoints:
		others = []

		for other in citypoints:
			if city == other:
				continue

			others.append((heuristic(city, other), other))

		others.sort(key=lambda item: item[0])

		for _, nearest in others[:connections_per_city]:
			pair = tuple(sorted([city, nearest]))
			road_pairs.add(pair)

	for start, goal in road_pairs:
		path = find_path(world, start, goal)

		if path:
			mark_road(world, path)

	return world