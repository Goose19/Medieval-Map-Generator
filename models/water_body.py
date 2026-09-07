class WaterBody:
	def __init__(self, water_body_id, name, water_type, territory, parent_id=None):
		self.id = water_body_id
		self.name = name
		self.water_type = water_type
		self.territory = territory
		self.parent_id = parent_id

	@property
	def area(self):
		return len(self.territory)