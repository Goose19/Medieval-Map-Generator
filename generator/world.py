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
		self.regions = []

		self.history = []