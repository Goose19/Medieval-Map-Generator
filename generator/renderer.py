BIOME_SYMBOLS = {
	"water": "~",
	"plains": ".",
	"dry_plains": ",",
	"forest": "F",
	"mountain": "^",
	"tundra": "t",
	"taiga": "T",
	"desert": "D",
	"jungle": "J",
	"river": "#",
	"city": "C"
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