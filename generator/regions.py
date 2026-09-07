import math

from models.province import Province
from models.region import Region
from generator.names import NameGenerator

def distance(a,b):
    ax, ay = a
    bx, by = b

    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

def create_provinces(world, name_generator):
    world.provinces = []

    province_number = 1

    for kingdom in world.kingdoms:
        kingdom.provinces = []

        for city in kingdom.cities:
            province = Province(province_id=f"province_{province_number}", name=name_generator.generate_province_name(), kingdom=kingdom, capital=city)

            city["province_id"] = province.id

            kingdom.provinces.append(province)
            world.provinces.append(province)

            province_number += 1
        

def assign_province_territories(world):
    for province in world.provinces:
        province.territory = []

    for kingdom in world.kingdoms:
        if not kingdom.provinces:
            continue

        for x, y in kingdom.territory:
            nearest_province = None
            nearest_distance = None

            for province in kingdom.provinces:
                capital = province.capital
                current_distance = distance((x, y), (capital["x"], capital["y"]))

                if nearest_distance is None or current_distance < nearest_distance:
                    nearest_distance = current_distance
                    nearest_province = province
                
            if nearest_province is None:
                continue
            
            nearest_province.territory.append((x, y))
            world.tiles[y][x].province_id = nearest_province.id

def get_region_count(province_count):
    if province_count <= 3:
        return 1
    
    return math.ceil(province_count / 3)

def get_province_position(province):
    return province.capital["x"], province.capital["y"]

def choose_region_centers(kingdom, count):
    if not kingdom.provinces:
        return []
    
    capital_province = None

    for province in kingdom.provinces:
        if province.capital == kingdom.capital:
            capital_province = province
            break
        
    if capital_province is None:
        capital_province = kingdom.provinces[0]
        
    centers = [capital_province]

    while len(centers) < count:
        best_province = None
        best_distance = -1

        for province in kingdom.provinces:
            if province in centers:
                continue
                
            position = get_province_position(province)
            distance_to_nearest_center = None

            for center in centers:
                center_position = get_province_position(center)
                current_distance = distance(position, center_position)

                if distance_to_nearest_center is None:
                    distance_to_nearest_center = current_distance
                    
                if current_distance < distance_to_nearest_center:
                    distance_to_nearest_center = current_distance

            if distance_to_nearest_center > best_distance:
                best_distance = distance_to_nearest_center
                best_province = province
            
        if best_province is None:
            break
            
        centers.append(best_province)
        
    return centers

def group_provinces_into_regions(kingdom):
    province_count = len(kingdom.provinces)
    region_count = get_region_count(len(kingdom.provinces))
    centers = choose_region_centers(kingdom, region_count)

    if not centers:
        return []

    groups = []

    for center in centers:
        groups.append([])

    for province in kingdom.provinces:
        position = get_province_position(province)

        nearest_index = 0
        nearest_distance = None

        i = 0

        for center in centers:
            center_position = get_province_position(center)
            current_distance = distance(position, center_position)

            if nearest_distance is None:
                nearest_distance = current_distance
                nearest_index = i
            
            if current_distance < nearest_distance:
                nearest_distance = current_distance
                nearest_index = i
            
            i += 1
        
        groups[nearest_index].append(province)
    
    return groups

def choose_region_capital(kingdom, provinces):
    for province in provinces:
        if province.capital is kingdom.capital:
            return province.capital
    
    best_province = None
    best_score = None

    for province in provinces:
        capital = province.capital
        score = capital.get("score", 0)

        if best_score is None:
            best_province = province
            best_score = score
        
        if score > best_score:
            best_province = province
            best_score = score
        
    if best_province is None:
        return None

    return best_province.capital

def create_regions(world, name_generator):
    world.regions = []

    region_number = 1

    for kingdom in world.kingdoms:
        kingdom.regions = []

        groups = group_provinces_into_regions(kingdom)

        for provinces in groups:
            region_id = f"region_{region_number}"
            region_name = name_generator.generate_region_name()

            region = Region(region_id=region_id, name=region_name, kingdom=kingdom)

            region.provinces = provinces
            region.capital = choose_region_capital(kingdom, provinces)

            for province in provinces:
                province.region = region

                for territory_position in province.territory:
                    x = territory_position[0]
                    y = territory_position[1]

                    region.territory.append((x, y))
                    world.tiles[y][x].region_id = region.id
            
            kingdom.regions.append(region)
            world.regions.append(region)

            region_number += 1

def detect_political_borders(world):
	for row in world.tiles:
		for tile in row:
			tile.region_border = False
			tile.kingdom_border = False

	directions = [
		(-1, 0),
		(1, 0),
		(0, -1),
		(0, 1)
	]

	for y in range(world.height):
		for x in range(world.width):
			tile = world.tiles[y][x]

			if tile.kingdom_id is None:
				continue

			for direction in directions:
				dx = direction[0]
				dy = direction[1]

				nx = x + dx
				ny = y + dy

				if nx < 0:
					continue

				if ny < 0:
					continue

				if nx >= world.width:
					continue

				if ny >= world.height:
					continue

				neighbor_tile = world.tiles[ny][nx]

				if neighbor_tile.kingdom_id is None:
					continue

				if tile.kingdom_id != neighbor_tile.kingdom_id:
					tile.kingdom_border = True
					continue

				if tile.region_id != neighbor_tile.region_id:
					tile.region_border = True

def determine_region_types(world):
    for region in world.regions:
        region.region_type = "inner"

        if region.capital is region.kingdom.capital:
            region.region_type = "capital"
            continue
        
        is_border_region = False
        is_coastal_region = False

        for territory_position in region.territory:
            x = territory_position[0]
            y = territory_position[1]

            tile = world.tiles[y][x]

            if tile.biome == "water":
                is_coastal_region = True
            
            if tile.biome == "deep_water":
                is_coastal_region = True
            
            neighbor_positions = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            ]

            for neighbor_position in neighbor_positions:
                nx = neighbor_position[0]
                ny = neighbor_position[1]

                if nx < 0:
                    continue
                
                if ny < 0:
                    continue
                
                if nx >= world.width:
                    continue
                
                if ny >= world.height:
                    continue
                
                neighbor_tile = world.tiles[ny][nx]

                if neighbor_tile.kingdom_id is None:
                    continue
                
                if neighbor_tile.kingdom_id != tile.kingdom_id:
                    is_border_region = True
                
                if neighbor_tile.biome == "water":
                    is_coastal_region = True

                if neighbor_tile.biome == "deep_water":
                    is_coastal_region = True
        
        if is_border_region:
            region.region_type = "border"
            continue
        
        if is_coastal_region:
            region.region_type = "coastal"
            continue

def generate_regions(world):
    name_generator = NameGenerator(world.seed)

    create_provinces(world, name_generator)
    assign_province_territories(world)
    create_regions(world, name_generator)
    determine_region_types(world)
    detect_political_borders(world)

    return world