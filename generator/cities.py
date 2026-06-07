import random

city_prefixes = [
    "North", "West", "East", "South",
    "Stone", "River", "High", "Old",
    "Red", "White", "Iron", "Green"
]

city_suffixes = [
    "ford", "helm", "hold", "wick",
    "bridge", "fall", "watch", "keep",
    "ton", "burg", "haven", "rest"
]

def generate_city_name():
    prefix = random.choice(city_prefixes)
    suffix = random.choice(city_suffixes)

    return prefix + suffix

WATER_BIOMES = ["water", "river"]


def get_tiles_in_radius(world, x, y, radius):
    tiles = []

    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            nx = x + dx
            ny = y + dy

            if 0 <= nx < world.width and 0 <= ny < world.height:
                tiles.append((nx, ny, world.tiles[ny][nx]))

    return tiles


def is_near_water(world, x, y, radius=3):
    for nx, ny, tile in get_tiles_in_radius(world, x, y, radius):
        if tile.biome in WATER_BIOMES:
            return True

    return False


def distance(a, b):
    ax, ay = a
    bx, by = b

    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5


def get_city_score(tile):
    if tile.biome == "plains":
        return 10

    if tile.biome == "forest":
        return 7

    if tile.biome == "dry_plains":
        return 5

    if tile.biome == "taiga":
        return 4

    if tile.biome == "tundra":
        return 3

    if tile.biome == "mountain":
        return 1

    return 0


def generate_cities(world, count=8):
    random.seed(world.seed + 3000)

    candidates = []

    for y in range(world.height):
        for x in range(world.width):
            tile = world.tiles[y][x]

            if tile.biome in ["water", "river", "city"]:
                continue

            # if not is_near_water(world, x, y):
            #     continue

            score = get_city_score(tile)

            if score <= 0:
                continue

            near_water = is_near_water(world, x, y)

            if not near_water and random.random() > 0.20:
                continue

            if near_water:
                score += 3

            

            # Горные поселения редкие.
            if tile.biome == "mountain" and random.random() > 0.12:
                continue

            # candidates.append((score, x, y))

            center_x = world.width / 2
            center_y = world.height / 2

            distance_from_center = distance(
                (x, y),
                (center_x, center_y)
            )

            score += distance_from_center * 0.03

            candidates.append((score, x, y))

    random.shuffle(candidates)
    candidates.sort(reverse=True)

    min_city_distance = 8
    created = 0

    for score, x, y in candidates:
        if created >= count:
            break

        too_close = False

        for city in world.cities:
            if distance((x, y), (city["x"], city["y"])) < min_city_distance:
                too_close = True
                break

        if too_close:
            continue

        tile = world.tiles[y][x]
        tile.biome = "city"

        world.cities.append({
            "name": generate_city_name(),
            "x": x,
            "y": y,
            "score": score
        })

        created += 1

    return world