from typing import List
from dataclasses import dataclass
from test_data.filter_data import Filter
from typing import Final

@dataclass
class Product:
    id : int
    name: str
    price : float
    description: str
    image_path: str

    
    @classmethod
    def sort_products(cls, products: List["Product"], filter_option: "Filter") -> List["Product"]:
        if filter_option in [Filter.NAME_ASC, Filter.NAME_DESC]:
            reverse = filter_option == Filter.NAME_DESC
            return sorted(products, key=lambda p: p.name, reverse=reverse)
        
        elif filter_option in [Filter.PRICE_ASC, Filter.PRICE_DESC]:
            reverse = filter_option == Filter.PRICE_DESC
            return sorted(products, key=lambda p: p.price, reverse=reverse)
        
        return products  # fallback if unknown filter

PRODUCTS : Final = [
    Product(
        id = 1, 
        name="Sauce Labs Backpack",
        price=29.99,
        description="carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",
        image_path="/static/media/sauce-backpack-1200x1500.0a0b85a385945026062b.jpg"
    ),
    Product(
        id = 2,
        name="Sauce Labs Bike Light",
        price=9.99,
        description="A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
        image_path="/static/media/bike-light-1200x1500.37c843b09a7d77409d63.jpg"
    ),
    Product(
        id = 3,
        name="Sauce Labs Bolt T-Shirt",
        price=15.99,
        description="Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.",
        image_path="/static/media/bolt-shirt-1200x1500.c2599ac5f0a35ed5931e.jpg"
    ),
    Product(
        id = 4,
        name="Sauce Labs Fleece Jacket",
        price=49.99,
        description="It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office.",
        image_path="/static/media/sauce-pullover-1200x1500.51d7ffaf301e698772c8.jpg"
    ),
    Product(
        id = 5,
        name="Sauce Labs Onesie",   
        price=7.99,
        description="Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",
        image_path="/static/media/red-onesie-1200x1500.2ec615b271ef4c3bc430.jpg"
    ),
    Product(
        id = 6,
        name="Test.allTheThings() T-Shirt (Red)",
        price=15.99,
        description="This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton.",
        image_path  ="/static/media/red-tatt-1200x1500.30dadef477804e54fc7b.jpg"
    )
]



allowed_cart = {
    "Sauce Labs Backpack": True,
    "Sauce Labs Bike Light": True,
    "Sauce Labs Bolt T-Shirt": False,
    "Sauce Labs Fleece Jacket": False,
    "Sauce Labs Onesie": True,
    "Test.allTheThings() T-Shirt (Red)": False
}
