import random

from generator.cities import is_near_water

BIOME_RURAL_DENSITY = {
	"plains": 130,
	"forest": 75,
	"dry_plains": 55,
	"taiga": 40,
	"tundra": 12,
	"mountain": 18,
	"desert": 10,
	"jungle": 35
}

BIOME_URBAN_MULTIPLIER = {
	"plains": 1.20,
	"forest": 1.00,
	"dry_plains": 0.85,
	"taiga": 0.75,
	"tundra": 0.55,
	"mountain": 0.65,
	"desert": 0.60,
	"jungle": 0.80
}

CULTURE_RURAL_MULTIPLIER = {
	"lowland": 1.10,
	"woodland": 1.00,
	"northern": 0.85,
	"highland": 0.90,
	"steppe": 0.80,
	"southern": 0.95,
	"maritime": 0.90
}

CULTURE_URBAN_MULTIPLIER = {
	"lowland": 1.10,
	"woodland": 0.95,
	"northern": 0.90,
	"highland": 0.90,
	"steppe": 0.85,
	"southern": 1.05,
	"maritime": 1.25
}

def clamp(value, minimum, maximum):
	return max(minimum, min(maximum, value))

def get_tile_rural_population(tile):
	if tile.biome in ["water", "river", "city"]:
		return 0.0

	base = BIOME_RURAL_DENSITY.get(tile.biome, 20)
	moisture_factor = 0.80 + tile.moisture * 0.35
	temperature_factor = clamp(1.05 - abs(tile.temperature - 0.55) * 0.65, 0.65, 1.05)

	return base * moisture_factor * temperature_factor

def get_city_population(world, city, kingdom, rng):
	biome = city.get("biome", "plains")
	score_factor = clamp(city.get("score", 8) / 10.0, 0.50, 1.50)

	population = 2200 * score_factor
	population *= BIOME_URBAN_MULTIPLIER.get(biome, 0.80)
	population *= CULTURE_URBAN_MULTIPLIER.get(kingdom.culture, 1.0)

	if is_near_water(world, city["x"], city["y"], radius=3):
		population *= 1.20

	if city is kingdom.capital:
		population *= 1.75

	population *= rng.uniform(0.90, 1.10)

	return max(500, int(round(population / 100.0) * 100))

def generate_population(world):
	rng = random.Random(world.seed + 5000)

	for kingdom in world.kingdoms:
		rural_population = 0.0

		for x, y in kingdom.territory:
			tile = world.tiles[y][x]
			tile_population = get_tile_rural_population(tile)

			if tile_population <= 0:
				continue

			if is_near_water(world, x, y, radius=2):
				tile_population *= 1.12

			rural_population += tile_population

		rural_population *= CULTURE_RURAL_MULTIPLIER.get(kingdom.culture, 1.0)

		kingdom.rural_population = int(round(rural_population / 100.0) * 100)
		kingdom.urban_population = 0

		for city in kingdom.cities:
			city["population"] = get_city_population(world, city, kingdom, rng)
			kingdom.urban_population += city["population"]

		kingdom.population = kingdom.rural_population + kingdom.urban_population

	return world