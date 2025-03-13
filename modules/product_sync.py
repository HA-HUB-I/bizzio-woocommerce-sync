from modules.xml_parser import BizzioXMLParser
from modules.woo_api import WooCommerceAPI
from modules.bizzio_api import BizzioAPI

def sync_products():
    """Извлича и синхронизира продукти, включително изображения и файлове"""
    bizzio_api = BizzioAPI()
    xml_source = bizzio_api.get_articles()

    if xml_source is None:
        print("🔴 Няма XML отговор от Bizzio API!")
        return

    parser = BizzioXMLParser(xml_source)
    woo_api = WooCommerceAPI()

    for batch in parser.get_products(batch_size=50):  # Обработваме по 50 продукта наведнъж
        print(f"🚀 Изпращане на партида от {len(batch)} продукта към WooCommerce...")
        for product in batch:
            woo_api.create_product(product)

    print("✅ Синхронизацията завърши успешно!")


def sync_products_batch():
    """Извлича и синхронизира продукти чрез WooCommerce batch API"""
    bizzio_api = BizzioAPI()
    xml_source = bizzio_api.get_articles()

    if xml_source is None:
        print("🔴 Няма XML отговор от Bizzio API!")
        return

    parser = BizzioXMLParser(xml_source)
    woo_api = WooCommerceAPI()

    for batch in parser.get_products(batch_size=100):  # Обработваме по 100 продукта
        print(f"🚀 Обработка на партида от {len(batch)} продукта...")

        create_list = []
        update_list = []
        delete_list = []  # Можем да добавим логика за изтриване, ако е нужно

       # Извличане на всички съществуващи продукти по SKU наведнъж
        existing_products = woo_api.get_products_by_skus([p["barcode"] for p in batch])   

        # # Разделяне на изображения и файлове
        # images = [file["url"] for file in product["files"] if file["url"].endswith((".png", ".jpg", ".jpeg"))]
        # files = [file for file in product["files"] if not file["url"].endswith((".png", ".jpg", ".jpeg"))]

        # # Обработка на изображенията (първото става основно)
        # product_images = [{"src": images[0]}] if images else []
        # if len(images) > 1:
        #     product_images += [{"src": img} for img in images[1:]]

         # Добавяне на мета полета за`
        meta_data = []    

        # # Добавяне на файлове като мета линкове
        # for file in files:
        #     meta_data.append({"key": f"file_{file['name']}", "value": file["url"]})         

        for product in batch:
            product_data = {
                "name": product["name"],
                "sku": product["barcode"],
                "regular_price": str(product["price"]),
                "stock_quantity": product["qty"],
                "categories": [{"id": 5}],  # Променете ID ако е нужно
                "meta_data": [{"key": f"prop_{i}", "value": v} for i, v in enumerate(product["props"])],
                "meta_data": meta_data
            }

            # Проверяваме дали SKU вече съществува в WooCommerce
            existing_product = existing_products.get(product["barcode"])
            if existing_product:
                product_data["id"] = existing_product["id"]  # Добавяме ID за актуализация
                update_list.append(product_data)
            else:
                create_list.append(product_data)

        # Изпращаме batch заявка
        woo_api.batch_process_products(create_products=create_list, update_products=update_list)

    print("✅ Синхронизация с WooCommerce завърши успешно!")