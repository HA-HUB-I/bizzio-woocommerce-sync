import requests
from requests_oauthlib import OAuth1
from config.settings import WOO_API

class WooCommerceAPI:
    def __init__(self):
        self.base_url = WOO_API["BASE_URL"]
        self.auth = OAuth1(
            WOO_API["CONSUMER_KEY"],
            client_secret=WOO_API["CONSUMER_SECRET"]
        )

    def batch_process_products(self, create_products=[], update_products=[], delete_products=[]):
        """Обработва продукти в WooCommerce на партиди чрез batch API"""
        url = f"{self.base_url}/batch"
        payload = {
            "create": create_products,
            "update": update_products,
            "delete": delete_products
        }

        response = requests.post(url, json=payload, auth=self.auth)
        if response.status_code in [200, 201]:
            print(f"🟢 Успешна batch обработка: {response.status_code}")
            return response.json()
        else:
            print(f"🔴 Грешка при batch заявка: {response.status_code}")
            print(response.text)
            return None
    def get_product_by_sku(self, sku):
        """Търси продукт по SKU в WooCommerce"""
        url = f"{self.base_url}?sku={sku}"
        response = requests.get(url, auth=self.auth)

        if response.status_code == 200:
            products = response.json()
            return products[0] if products else None
        else:
            print(f"🔴 Грешка при търсене на SKU {sku}: {response.status_code}")
            return None
        

    def create_product(self, product):
        """Създава нов продукт в WooCommerce и добавя изображения, файлове и мета полета"""
        print(f"🛒 Изпращане на продукт към WooCommerce: {product['name']}")

        # Разделяне на изображения и файлове
        images = [file["url"] for file in product["files"] if file["url"].endswith((".png", ".jpg", ".jpeg"))]
        files = [file for file in product["files"] if not file["url"].endswith((".png", ".jpg", ".jpeg"))]

        # Обработка на изображенията (първото става основно)
        product_images = [{"src": images[0]}] if images else []
        if len(images) > 1:
            product_images += [{"src": img} for img in images[1:]]

        # Добавяне на мета полета за `props`
        meta_data = []
        for i, prop in enumerate(product["props"]):
            meta_data.append({"key": f"custom_prop_{i+1}", "value": prop})

        # Добавяне на файлове като мета линкове
        for file in files:
            meta_data.append({"key": f"file_{file['name']}", "value": file["url"]})

        # WooCommerce продуктови данни
        product_data = {
            "name": product["name"],
            "sku": product["barcode"],
            "regular_price": str(product["price"]),
            "stock_quantity": product["qty"],
            "categories": [{"id": 5}],  # Тук може да се динамично избира категория
            "images": product_images,
            "meta_data": meta_data
        }

        

        # Изпращане на заявка към WooCommerce
        response = requests.post(self.base_url, json=product_data, auth=self.auth)

        if response.status_code == 201:
            print("🟢 Продуктът е създаден успешно!")
            return response.json()
        else:
            print(f"🔴 Грешка при създаване на продукт! Код: {response.status_code}")
            print(response.text)
            return None
        
    
