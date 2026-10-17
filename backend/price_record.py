#price_record.py

#Represents a price listing for a single gunpla at a single store.

class price_record:
    def __init__(
        self,
        gunpla_id,
        store_id,
        price,
        availability,
        stock,
        product_url
    ):
        self.gunpla_id = gunpla_id
        self.store_id = store_id
        self.price = price
        self.availability = availability
        self.stock = stock
        self.product_url = product_url