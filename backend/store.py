#This is our store organizer code.

class Store:
    def __init__(self, name, website, marketplace = False, reliability = "Good"):
        self.name = name
        self.website = website
        self.marketplace = marketplace
        self.reliability = reliability