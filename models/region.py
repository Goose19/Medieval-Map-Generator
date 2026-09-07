class Region:
    def __init__(self, region_id, name, kingdom):
        self.id = region_id
        self.name = name
        self.kingdom = kingdom

        self.provinces = []
        self.territory = []

        self.capital = None
        self.region_type = "inner"