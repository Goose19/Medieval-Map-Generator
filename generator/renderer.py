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

REGION_SYMBOLS = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

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

def create_region_symbols(world):
	region_symbols = {}

	symbol_index = 0

	for region in world.regions:
		if symbol_index < len(REGION_SYMBOLS):
			symbol = REGION_SYMBOLS[symbol_index]
		else:
			symbol = "?"

		region_symbols[region.id] = symbol
		symbol_index += 1
	
	return region_symbols

def render_region_map(world):
	lines = []
	region_symbols = create_region_symbols(world)

	for row in world.tiles:
		line = ""

		for tile in row:
			if tile.biome == "deep_water":
				line += "≈"
				continue

			if tile.biome == "water":
				line += "~"
				continue

			if tile.biome == "river":
				line += "#"
				continue
			
			if tile.biome == "bridge":
				line += "+"
				continue

			if tile.region_id is not None:
				symbol = region_symbols.get(tile.region_id, "?")
				line += symbol
				continue

			line += "."

		lines.append(line)

	return "\n".join(lines)

def print_region_map(world):
	print(render_region_map(world))

def print_region_legend(world):
	region_symbols = create_region_symbols(world)

	print()
	print("Region Legend:")
	for region in world.regions:
		symbol = region_symbols.get(region.id, "?")
		print(f"{symbol} - {region.name} ({region.kingdom.name})")

def render_border_map(world):
	lines = []

	for row in world.tiles:
		line = ""

		for tile in row:
			if tile.biome == "deep_water":
				line += "="
				continue
			
			if tile.biome == "water":
				line += "~"
				continue

			if tile.biome == "river":
				line += "#"
				continue
			
			if tile.biome == "bridge":
				line += "+"
				continue
			
			if tile.kingdom_border:
				line += "K"
				continue
			
			if tile.region_border:
				line += "R"
				continue
			
			if tile.region_id is not None:
				line += "."
				continue
			
			line += " "

		lines.append(line)

	return "\n".join(lines)

def print_border_map(world):
	print(render_border_map(world))

CLIMATE_SYMBOLS = {
	"polar": "P",
	"subpolar": "B",
	"temperate": "T",
	"subtropical": "S",
	"tropical": "E"
}


def render_water_map(world):
	lines = []
	water_bodies = {water_body.id: water_body for water_body in world.water_bodies}

	for row in world.tiles:
		line = ""

		for tile in row:
			if tile.biome == "river":
				line += "#"
				continue

			if tile.biome == "bridge":
				line += "+"
				continue

			if tile.bay_id is not None:
				line += "B"
				continue

			if tile.water_body_id is not None:
				water_body = water_bodies.get(tile.water_body_id)

				if water_body is not None and water_body.water_type == "sea":
					line += "~"
					continue

				if water_body is not None and water_body.water_type == "lake":
					line += "O"
					continue

			line += "."

		lines.append(line)

	return "\n".join(lines)


def print_water_map(world):
	print(render_water_map(world))


def print_water_legend(world):
	water_bodies = {water_body.id: water_body for water_body in world.water_bodies}

	print()
	print("Water Legend:")
	print("~ - sea")
	print("O - lake")
	print("B - bay")
	print("# - river")
	print("+ - bridge")

	if world.seas:
		print()
		print("Seas:")

		for sea in world.seas:
			print(f"- {sea.name} ({sea.area} tiles)")

	if world.lakes:
		print()
		print("Lakes:")

		for lake in world.lakes:
			print(f"- {lake.name} ({lake.area} tiles)")

	if world.bays:
		print()
		print("Bays:")

		for bay in world.bays:
			parent = water_bodies.get(bay.parent_id)

			if parent is not None:
				print(f"- {bay.name} ({bay.area} tiles) — {parent.name}")

			else:
				print(f"- {bay.name} ({bay.area} tiles)")


def render_climate_map(world):
	lines = []

	for row in world.tiles:
		line = ""

		for tile in row:
			line += CLIMATE_SYMBOLS.get(tile.climate_zone, "?")

		lines.append(line)

	return "\n".join(lines)


def print_climate_map(world):
	print(render_climate_map(world))


def print_climate_legend():
	print()
	print("Climate Legend:")
	print("P - polar")
	print("B - subpolar")
	print("T - temperate")
	print("S - subtropical")
	print("E - tropical")


def print_geography_info(world):
	water_bodies = {water_body.id: water_body for water_body in world.water_bodies}

	print()
	print("geography:")
	print(f" Seas: {len(world.seas)}")
	print(f" Lakes: {len(world.lakes)}")
	print(f" Bays: {len(world.bays)}")

	for sea in world.seas:
		print(f" - Sea: {sea.name} — {sea.area} tiles")

	for lake in world.lakes:
		print(f" - Lake: {lake.name} — {lake.area} tiles")

	for bay in world.bays:
		parent = water_bodies.get(bay.parent_id)

		if parent is not None:
			print(f" - Bay: {bay.name} — {bay.area} tiles — parent: {parent.name}")

		else:
			print(f" - Bay: {bay.name} — {bay.area} tiles")