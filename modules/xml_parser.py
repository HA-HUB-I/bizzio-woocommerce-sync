import xml.etree.ElementTree as ET

class BizzioXMLParser:
    def __init__(self, xml_source):
        """Приема или XML текст, или файл"""
        if xml_source.endswith(".xml"):
            self.tree = ET.parse(xml_source)
            self.root = self.tree.getroot()
        else:
            self.root = ET.fromstring(xml_source)

    def get_products(self, batch_size=100):
        """Извлича продукти и обработва изображения, файлове и атрибути"""
        namespace = "{http://schemas.datacontract.org/2004/07/Bizzio.Srv.Extensions.RiznShop}"
        products = []
        count = 0

        for article in self.root.findall(f".//{namespace}AI"):
            product_data = {
                "barcode": article.find(f"{namespace}Barcode").text if article.find(f"{namespace}Barcode") is not None else None,
                "name": article.find(f"{namespace}Name").text if article.find(f"{namespace}Name") is not None else None,
                "price": float(article.find(f"{namespace}P_Sale").text) if article.find(f"{namespace}P_Sale") is not None else None,
                "qty": int(article.find(f"{namespace}Qty").text) if article.find(f"{namespace}Qty") is not None else 0,
                "props": [prop.text for prop in article.findall(f"{namespace}Props/*") if prop.text],  # Записва всички `b:string`
                "files": [
                    {
                        "id": file.find(f"{namespace}ID").text if file.find(f"{namespace}ID") is not None else None,
                        "name": file.find(f"{namespace}Name").text if file.find(f"{namespace}Name") is not None else None,
                        "url": file.find(f"{namespace}Uri").text if file.find(f"{namespace}Uri") is not None else None,
                    }
                    for file in article.findall(f"{namespace}Files/{namespace}FI")
                ],
            }
            products.append(product_data)
            count += 1

            if count % batch_size == 0:
                yield products  # Връща текущия batch
                products = []

        if products:
            yield products  # Връща оставащите продукти
