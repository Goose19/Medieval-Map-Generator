class Province:
    def __init__(self, province_id, name, kingdom, capital):
        self.id = province_id
        self.name = name
        self.kingdom = kingdom
        self.capital = capital

        self.cities = [capital]
        self.territory = []

        self.region = None