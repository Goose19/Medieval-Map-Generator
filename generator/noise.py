from noise import pnoise2


def normalize(value):
    return (value + 1) / 2


def generate_height(x, y, scale, seed):
    value = pnoise2(
        (x + seed * 13) / scale,
        (y + seed * 17) / scale,
        octaves = 5,
        persistence = 0.5,
        lacunarity = 2.0,
    )

    return normalize(value)


def generate_moisture(x, y, scale, seed):
    value = pnoise2(
        (x + seed * 31 + 5000) / scale,
        (y + seed * 37 + 5000) / scale,
        octaves = 4,
        persistence = 0.6,
        lacunarity = 2.0,
    )

    return normalize(value)

def generate_temperature(x, y, scale, seed):
	value = pnoise2(
		(x + seed * 41 + 9000) / scale,
		(y + seed * 43 + 9000) / scale,
		octaves = 3,
		persistence = 0.5,
		lacunarity = 2.0,
		)

	return normalize(value)