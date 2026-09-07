class Tile:
	def __init__(self, biome="plains", height = 0.0, moisture = 0.0, temperature=0.0):
		self.biome = biome
		self.height = height
		self.moisture = moisture
		self.temperature = temperature

		self.kingdom_id = None
		self.province_id = None
		self.region_id = None

		self.water_body_id = None
		self.bay_id = None
		self.climate_zone = None

		self.region_border = False
		self.kingdom_border = False