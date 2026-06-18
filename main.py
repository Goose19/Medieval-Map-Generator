import argparse

from generator.world import World
from generator.terrain import generate_terrain
from generator.renderer import print_world, print_layer
from generator.rivers import generate_rivers
from generator.cities import generate_cities
from generator.roads import connect_cities_with_roads
from generator.kingdoms import generate_kingdoms


def generate_command(args):
	world = World(
		width = args.width,
		height = args.height,
		seed = args.seed
		)

	generate_terrain(world)

	generate_rivers(world, count=args.rivers)

	generate_cities(world, count=args.cities)

	generate_kingdoms(world, count=3)

	connect_cities_with_roads(world)

	if args.mode == "biome":
		print_world(world)

	else:
		print_layer(world, args.mode)

	if args.show_kingdoms:
		print()
		print("kingdoms:")

		for kingdom in world.kingdoms:
			print(f"- {kingdom.name}")
			print(f" State type: {kingdom.state_type}")
			print(
				f" Capital: {kingdom.capital['name']} "
				f"({kingdom.capital['x']}, {kingdom.capital['y']})"
			)

			print(f" Territory size: {len(kingdom.territory)} tiles")

			print(" cities:")

			for city in kingdom.cities:
				print(
					f" - {city['name']} "
					f"({city['x']}, {city['y']})"
				)



def main():
	parser = argparse.ArgumentParser(
		description = "Medieval Map Generator"
		)

	subparsers = parser.add_subparsers(dest="command")

	generate_parser = subparsers.add_parser(
		"generate",
		help="Generate new world"
		)

	generate_parser.add_argument(
		"-w",
		"--width",
		type=int,
		required=True,
		help="Map width"
		)

	generate_parser.add_argument(
		"-H",
		"--height",
		type=int,
		required=True,
		help="Map height"
		)

	generate_parser.add_argument(
		"-s",
		"--seed",
		type=int,
		required=True,
		help="Map seed"
		)

	generate_parser.add_argument(
		"--mode",
		choices=["biome", "height", "moisture", "temperature"],
		default="biome",
		help="Render mode"
		)

	generate_parser.add_argument(
		"--rivers",
		type=int,
		default=8,
		help="Number of rivers"
		)

	generate_parser.add_argument(
		"--cities",
		type=int,
		default=8,
		help="Number of cities"
		)

	generate_parser.add_argument(
		"--show-kingdoms",
		action="store_true",
		help="Show kingdoms information"
		)

	args = parser.parse_args()

	if args.command == "generate":
		generate_command(args)

	else:
		parser.print_help()

if __name__ == "__main__":
	main()

# world = World(width=30, height=10, seed=12345)


# generate_terrain(world)

# print_world(world)


# for row in world.tiles:
# 	for tile in row:
# 		print(tile.biome[0], end="")
# 	print()