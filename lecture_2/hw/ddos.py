import requests
import random
import time

BASE_URL = "http://localhost:8000"

def create_items() -> None:
    url = f"{BASE_URL}/item"
    for i in range(100):
        name = f"Item {i}"
        price = round(random.uniform(5.0, 50.0), 2)
        data = {"name": name, "price": price}
        requests.post(url, json=data)
        time.sleep(0.3)

def create_carts() -> None:
    url = f"{BASE_URL}/cart"
    for _ in range(100):
        requests.post(url)
        time.sleep(0.3)


def add_items_to_carts() -> None:
    for cart_id in range(10):
        for item_id in range(10):
            requests.post(f"{BASE_URL}/cart/{cart_id}/add/{item_id}")
            time.sleep(0.3)


def get_cart() -> None:
    for cart_id in range(10):
        requests.get(f"{BASE_URL}/cart/{cart_id}")
        time.sleep(0.3)



def main():
    create_items()
    create_carts()
    add_items_to_carts()
    get_cart()

if __name__ == "__main__":
    main()