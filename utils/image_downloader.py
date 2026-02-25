import requests
import os
from dotenv import load_dotenv


from pathlib import Path
from test_data.product_data import PRODUCTS

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
IMAGE_PATH = os.getenv("IMAGE_PATH")

IMAGE_DIR = Path(IMAGE_PATH)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

def normalize_image_name(name: str) -> str: 
    import pdb
    pdb.set_trace()
    #takes O(k * n * m ) times
    # return (name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "")) + ".jpg"

    #takes O(n) time as lookup takes O(n * m ) , since m = 1 , Only O(n) time compl
    table = str.maketrans({
        " ": "_",
        "(": "",
        ")": "",
        ".": ""
    })

    cleaned = name.lower().translate(table) + ".jpg"
    return cleaned

def download_all_product_images():
    for product in PRODUCTS:
        image_url = BASE_URL + product.image_path
        filename = normalize_image_name(product.name)

        save_path = IMAGE_DIR / filename

        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        save_path.write_bytes(response.content)
        print(f"Saved: {save_path}")       
    


if __name__ == "__main__":
    download_all_product_images()