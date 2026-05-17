from models.tile import Tile
from generator.noise import generate_height, generate_moisture, generate_temperature

def resolve_biome(height, moisture, temperature):
    if height < 0.38:
        return "water"

    if height > 0.68:
        return "mountain"

    if temperature < 0.38:
        if moisture < 0.45:
            return "tundra"
        return "taiga"

    if temperature > 0.62:
        if moisture < 0.4:
            return "desert"
        return "jungle"

    if moisture < 0.35:
        return "dry_plains"

    if moisture < 0.58:
        return "plains"

    return "forest"


def generate_terrain(world):
    height_scale = 35.0
    moisture_scale = 25.0
    temperature_scale = 45.0

    world.tiles = []

    for y in range(world.height):
        row = []

        for x in range(world.width):
            height = generate_height(
                x,
                y,
                height_scale,
                world.seed
            )

            moisture = generate_moisture(
                x,
                y,
                moisture_scale,
                world.seed
            )

            temperature = generate_temperature(
                x,
                y,
                temperature_scale,
                world.seed
                )

            biome = resolve_biome(
                height,
                moisture,
                temperature
                )            

            row.append(Tile(
                biome,
                height,
                moisture,
                temperature
                )
            )

        world.tiles.append(row)

    return world