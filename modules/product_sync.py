from modules.xml_parser import BizzioXMLParser
from modules.woo_api import WooCommerceAPI
from modules.bizzio_api import BizzioAPI

def sync_products():
    """Извлича и синхронизира продукти на партиди (batch processing)"""
    bizzio_api = BizzioAPI()
    xml_source = bizzio_api.get_articles()

    if xml_source is None:
        print("🔴 Няма XML отговор от Bizzio API!")
        return

    parser = BizzioXMLParser(xml_source)
    woo_api = WooCommerceAPI()

    for batch in parser.get_products(batch_size=100):
        print(f"🚀 Изпращане на партида от {len(batch)} продукта към WooCommerce...")
        for product in batch:
            woo_api.create_product(product)

    print("✅ Синхронизацията завърши успешно!")
