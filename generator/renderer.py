BIOME_SYMBOLS = {
	"deep_water": "≈",
	"water": "~",
	"beach": ".",

	"plains": ",",
	"dry_plains": ";",
	"forest": "F",

	"jungle": "J",
	"tundra": "_",
	"taiga": "T",

	"swamp": "S",

	"hills": "n",
	"cold_hills": "N",
	"forest_hills": "H",

	"mountain": "^",
	"green_mountain": "A",
	"snow_mountain": "M",

	"desert": "D",

	"river": "#",
	"city": "C",
	"road": "=",
	"bridge": "+"
}

def render_ascii(world):
	lines = []

	for row in world.tiles:
		line = ""

		for tile in row:
			symbol = BIOME_SYMBOLS.get(tile.biome, "?")
			line += symbol

		lines.append(line)

	return "\n".join(lines)

def print_world(world):
	print(render_ascii(world))

def value_to_digit(value):
	return str(min(9, max(0, int(value * 10))))

def renderer_layer(world, layer_name):
	lines = []

	for row in world.tiles:
		line = ""

		for tile in row:
			value = getattr(tile, layer_name)
			line += value_to_digit(value)

		lines.append(line)

	return "\n".join(lines)

def print_layer(world, layer_name):
	print(renderer_layer(world, layer_name))