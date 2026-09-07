class World:
	def __init__(self, width, height, seed):
		self.width = width
		self.height = height
		self.seed = seed

		self.tiles = []

		self.rivers = []
		self.cities = []
		self.roads = []

		self.kingdoms = []
		self.provinces = []
		self.regions = []

		self.water_bodies = []
		self.seas = []
		self.lakes = []
		self.bays = []

		self.history = []