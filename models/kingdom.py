class Kingdom:
	def __init__(self, kingdom_id, name, capital=None, state_type="kingdom", culture="lowland"):
		self.id = kingdom_id
		self.name = name
		self.capital = capital
		self.state_type = state_type
		self.culture = culture

		self.cities = []
		self.territory = []
		
		self.provinces = []
		self.regions = []

		self.neighbors = []
		self.border_lengths = {}

		self.relations = {}

		self.population = 0
		self.urban_population = 0
		self.rural_population = 0
		self.wealth = 0
		self.military_power = 0
		self.stability = 0

		self.color = None