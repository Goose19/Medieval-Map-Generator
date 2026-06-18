class Kingdom:
	def __init__(self, name, capital=None, state_type="kingdom"):
		self.name = name
		self.capital = capital
		self.state_type = state_type

		self.cities = []
		self.territory = []

		self.population = 0
		self.wealth = 0
		self.military_power = 0
		self.stability = 0

		self.color = None