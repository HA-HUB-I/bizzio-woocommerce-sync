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

    def create_product(self, product):
        """Създава нов продукт в WooCommerce с OAuth 1.0"""
        print(f"🛒 Изпращане на продукт към WooCommerce: {product['name']}")
        
        response = requests.post(self.base_url, json=product, auth=self.auth)
        
        if response.status_code == 201:
            print("🟢 Продуктът е създаден успешно!")
            return response.json()
        else:
            print(f"🔴 Грешка при създаване на продукт! Код: {response.status_code}")
            print(response.text)
            return None

    def update_product(self, product_id, update_data):
        """Актуализира съществуващ продукт"""
        response = requests.put(f"{self.base_url}/{product_id}", json=update_data, auth=self.auth)
        
        if response.status_code == 200:
            print("🟢 Продуктът е актуализиран успешно!")
            return response.json()
        else:
            print(f"🔴 Грешка при обновяване на продукт! Код: {response.status_code}")
            print(response.text)
            return None
