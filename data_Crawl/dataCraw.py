import requests
import json
import os
from datetime import datetime

# Cấu hình
category_id = 5991
total_pages = 130
landing_zone = "landing_zone"
os.makedirs(landing_zone, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_products = []

for page in range(1, total_pages + 1):
    url = "https://www.fahasa.com/fahasa_catalog/product/loadproducts"
    params = {
        "category_id": category_id,
        "currentPage": page,
        "limit": 24,
        "order": "created_at",
        "series_type": 0
    }
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        raw_data = response.json()
        product_list = raw_data.get("product_list", [])

        for product in product_list:
            all_products.append({
                "product_id": product.get("product_id"),
                "product_name": product.get("product_name"),
                "product_finalprice": product.get("product_finalprice"),
                "product_price": product.get("product_price"),
                "discount": product.get("discount"),
                "product_url": product.get("product_url"),
                "image_src": product.get("image_src"),
            })
        print(f"Collected page {page}")
    else:
        print(f"Failed to get page {page}: {response.status_code}")
output_file = os.path.join(
    landing_zone,"fahasa_data.json"
)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=4)

print(f"Done! Total products: {len(all_products)}")
print(f"📁 Output saved to: {output_file}")
