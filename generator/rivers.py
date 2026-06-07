import random

DIRECTIONS = [
(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (-1,1), (1,1)
]

def get_neighbors(world, x, y):
    neighbors = []

    for dx, dy in DIRECTIONS:
        nx = x + dx
        ny = y + dy

        if 0 <= nx < world.width and 0 <= ny < world.height:
            neighbors.append((nx,ny))

    return neighbors

def find_sources(world, min_height=0.60):
    sources = []

    for y in range(world.height):
        for x in range(world.width):
            tile = world.tiles[y][x]

            if tile.height >= min_height and tile.biome not in ["water", "river"]:
                # if tile.biome in ["mountain", "taiga", "tundra"]:
                if tile.biome not in ["desert", "jungle"]:
                    sources.append((x,y))

    return sources

def choose_next_tile(world, x, y, visited):
    current = world.tiles[y][x]
    candidates = []

    for nx, ny in get_neighbors(world, x, y):
        if (nx,ny) in visited:
            continue

        neighbor = world.tiles[ny][nx]

        if neighbor.biome == "mountain":
            continue

        heightdiff = current.height - neighbor.height

        if heightdiff >= -0.015:
            score = neighbor.height

            score -= heightdiff * 0.35

            if nx != x and ny != y:
                score += 0.01

            candidates.append((score, nx, ny))

        # if neighbor.height <= current.height + 0.01:
        #     candidates.append((neighbor.height,nx,ny))

    if not candidates:
        return None

    candidates.sort(key=lambda item: item[0])

    best_height = candidates[0][0]

    best_candidates = []

    for height, nx, ny in candidates:
        if height <= best_height + 0.015:
            best_candidates.append((height,nx,ny))

    _, next_x, next_y = random.choice(best_candidates)

    return next_x, next_y

def carve_river(world, start_x, start_y, max_length=300):
    x = start_x
    y = start_y

    path = []
    visited = set()
    reached_water = False

    for _ in range(max_length):
        current = world.tiles[y][x]

        if current.biome == "water":
            reached_water = True
            break

        if (x, y) in visited:
            break

        visited.add((x,y))
        path.append((x,y))

        next_tile = choose_next_tile(world, x, y, visited)

        if next_tile is None:
            break

        x, y = next_tile

    if len(path) < 5 or not reached_water:
        return None

    for rx, ry in path:
        tile = world.tiles[ry][rx]

        # if tile.biome != "water" and tile.biome != "mountain":
        if tile.biome != "water":
            tile.biome = "river"

    return path


def generate_rivers(world, count=8):
    random.seed(world.seed + 2000)

    sources = find_sources(world)

    if not sources:
        return world

    random.shuffle(sources)

    created = 0

    used_sources = []
    min_source_distance = 12

    for source_x, source_y in sources:
        if created >= count:
            break

        too_close = False

        for used_source in used_sources:
            if distance((source_x, source_y), used_source) < min_source_distance:
                too_close = True
                break

        if too_close:
            continue

        path = carve_river(world, source_x, source_y)

        if path is not None:
            world.rivers.append(path)
            used_sources.append((source_x,source_y))
            created += 1

    return world

def distance(a, b):
    ax, ay = a
    bx, by = b

    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5