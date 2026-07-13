from dataclasses import dataclass
from datetime import datetime

@dataclass
class Ordine:
    order_id: int
    customer_id: int
    order_status: int
    order_date: datetime
    required_date: datetime
    shipped_date: datetime
    store_id: int
    staff_id: int

    def __hash__(self):
        return hash(self. order_id)

    def __str__(self):
        return f" ordine:{self. order_id} cliente- {self.customer_id})- stato:{self.order_status}"

    def __eq__(self, other):
        return self. order_id == other. order_id