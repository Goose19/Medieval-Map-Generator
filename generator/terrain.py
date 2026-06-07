from models.tile import Tile
from generator.noise import generate_height, generate_moisture, generate_temperature

def clamp(value, min_value=0.0, max_value=1.0):
    return max(min_value, min(max_value, value))

def apply_latitude_temperature(y, world_height, noise_temperature):
    latitude = y / max(1, world_height - 1)

    latitude_temperature = latitude

    temperature = latitude_temperature * 0.60 + noise_temperature * 0.40

    return clamp(temperature)

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
        if moisture < 0.35:
            return "desert"
        
        if moisture > 0.70:
            return "jungle"

        return "plains"

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

            noise_temperature = generate_temperature(
                x,
                y,
                temperature_scale,
                world.seed
            )

            temperature = apply_latitude_temperature(
                y,
                world.height,
                noise_temperature
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