import random


CULTURE_AFFINITY = {
	("lowland", "maritime"): 8,
	("lowland", "woodland"): 6,
	("woodland", "highland"): 6,
	("northern", "highland"): 8,
	("steppe", "lowland"): 4,
	("southern", "maritime"): 8
}


def clamp(value, minimum, maximum):
	return max(minimum, min(maximum, value))


def get_culture_modifier(kingdom_a, kingdom_b):
	if kingdom_a.culture == kingdom_b.culture:
		return 15

	pair = tuple(sorted((kingdom_a.culture, kingdom_b.culture)))

	for cultures, modifier in CULTURE_AFFINITY.items():
		if tuple(sorted(cultures)) == pair:
			return modifier

	return 0


def get_state_type_modifier(kingdom_a, kingdom_b):
	modifier = 0

	if kingdom_a.state_type == kingdom_b.state_type:
		modifier += 4

	republic_types = ["republic", "free_city"]

	if kingdom_a.state_type in republic_types and kingdom_b.state_type in republic_types:
		modifier += 8

	if kingdom_a.state_type == "empire":
		modifier -= 6

	if kingdom_b.state_type == "empire":
		modifier -= 6

	if kingdom_a.state_type == "empire" and kingdom_b.state_type == "empire":
		modifier -= 10

	return modifier


def get_border_modifier(kingdom_a, kingdom_b):
	if kingdom_b not in kingdom_a.neighbors:
		return 0

	border_length = kingdom_a.border_lengths.get(kingdom_b.name, 0)

	modifier = 6
	modifier -= min(border_length * 0.35, 18)

	return modifier


def get_population_modifier(kingdom_a, kingdom_b):
	smaller_population = min(kingdom_a.population, kingdom_b.population)
	larger_population = max(kingdom_a.population, kingdom_b.population)

	if smaller_population <= 0:
		return 0

	ratio = larger_population / smaller_population

	if ratio >= 4:
		return -8

	if ratio >= 2.5:
		return -4

	return 0


def get_relation_status(score):
	if score >= 40:
		return "friendly"

	if score >= 15:
		return "cordial"

	if score > -15:
		return "neutral"

	if score > -40:
		return "tense"

	return "hostile"


def calculate_relation(world, kingdom_a, kingdom_b, rng):
	score = 0.0

	score += get_culture_modifier(kingdom_a, kingdom_b)
	score += get_state_type_modifier(kingdom_a, kingdom_b)
	score += get_border_modifier(kingdom_a, kingdom_b)
	score += get_population_modifier(kingdom_a, kingdom_b)

	score += rng.uniform(-18, 18)
	score = int(round(clamp(score, -100, 100)))

	return score


def generate_relations(world):
	rng = random.Random(world.seed + 6000)

	for kingdom in world.kingdoms:
		kingdom.relations = {}

	for i in range(len(world.kingdoms)):
		for j in range(i + 1, len(world.kingdoms)):
			kingdom_a = world.kingdoms[i]
			kingdom_b = world.kingdoms[j]

			score = calculate_relation(world, kingdom_a, kingdom_b, rng)
			status = get_relation_status(score)

			kingdom_a.relations[kingdom_b.name] = {
				"score": score,
				"status": status
			}

			kingdom_b.relations[kingdom_a.name] = {
				"score": score,
				"status": status
			}

	return world