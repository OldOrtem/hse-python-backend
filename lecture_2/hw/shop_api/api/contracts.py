from typing import Any, Dict, List
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool = False

    def as_responce(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "price": self.price}


class CreateItem(BaseModel):
    name: str
    price: float

class CartItem(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool = True


class Cart(BaseModel):
    id: int
    items: List[CartItem] = []
    price: float = 0.0

    def add(self, item: Item):
        for cart_item in self.items:
            if cart_item.id == item.id:
                cart_item.quantity += 1
                break
        else:
            self.items.append(CartItem(id=item.id, name=item.name, quantity=1))
        self.price += item.price

    def as_responce(self) -> Dict[str, Any]:
        return self.model_dump()