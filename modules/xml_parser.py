import xml.etree.ElementTree as ET

class BizzioXMLParser:
    def __init__(self, xml_source):
        """Приема или XML текст, или файл"""
        if xml_source.endswith(".xml"):
            self.tree = ET.parse(xml_source)
            self.root = self.tree.getroot()
        else:
            self.root = ET.fromstring(xml_source)

    def safe_get_text(self, element):
        """Безопасно извличане на текст от XML елемент, избягвайки грешки"""
        return element.text.strip() if element is not None and element.text else ""

    def get_products(self, batch_size=100):
        """Извлича продукти и обработва безопасно числовите стойности"""
        namespace = "{http://schemas.datacontract.org/2004/07/Bizzio.Srv.Extensions.RiznShop}"
        products = []
        count = 0

        for article in self.root.findall(f".//{namespace}AI"):
            try:
                qty_value = self.safe_get_text(article.find(f"{namespace}Qty"))
                qty = round(float(qty_value)) if qty_value.replace(".", "").isdigit() else 0  # Конвертираме правилно

                product_data = {
                    "barcode": self.safe_get_text(article.find(f"{namespace}Barcode")),
                    "name": self.safe_get_text(article.find(f"{namespace}Name")),
                    "price": float(self.safe_get_text(article.find(f"{namespace}P_Sale")) or 0),
                    "qty": qty,  # Закръгляне на наличността до цяло число
                    "props": [prop.text for prop in article.findall(f"{namespace}Props/*") if prop.text],
                    "files": [
                        {
                            "id": self.safe_get_text(file.find(f"{namespace}ID")),
                            "name": self.safe_get_text(file.find(f"{namespace}Name")),
                            "url": self.safe_get_text(file.find(f"{namespace}Uri")),
                        }
                        for file in article.findall(f"{namespace}Files/{namespace}FI")
                    ],
                }

                products.append(product_data)
                count += 1

                if count % batch_size == 0:
                    yield products  # Връща текущия batch
                    products = []

            except Exception as e:
                print(f"⚠️ Грешка при обработка на продукт: {e}. Пропускане на този запис...")

        if products:
            yield products  # Връща оставащите продукти
