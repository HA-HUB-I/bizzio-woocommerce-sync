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

        for product in batch:
            product_data = {
                "name": product["name"],
                "sku": product["barcode"],
                "regular_price": str(product["price"]),
                "stock_quantity": product["qty"],
                "categories": [{"id": 5}],  # Променете ID ако е нужно
                "meta_data": [{"key": f"prop_{i}", "value": v} for i, v in enumerate(product["props"])],
            }

            # Проверяваме дали продуктът съществува
            existing_product = woo_api.get_product_by_sku(product["barcode"])
            if existing_product:
                product_data["id"] = existing_product["id"]
                update_list.append(product_data)
            else:
                create_list.append(product_data)

        # Изпращаме batch заявка
        woo_api.batch_process_products(create_products=create_list, update_products=update_list, delete_products=delete_list)

    print("✅ Синхронизация с WooCommerce завърши успешно!")