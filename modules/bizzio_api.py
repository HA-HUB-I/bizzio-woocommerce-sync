import requests
from config.settings import BIZZIO_API

class BizzioAPI:
    def __init__(self):
        self.base_url = BIZZIO_API["BASE_URL"]
        self.auth = BIZZIO_API

    def get_articles(self, modified_after=None):
        """Извлича артикули от Bizzio API и ги записва в XML файл при голям отговор"""
        print("🔗 Изпращане на заявка към Bizzio API...")

        payload = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/" xmlns:biz="http://schemas.datacontract.org/2004/07/Bizzio.Srv.Extensions.RiznShop" 
                         xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
                <soapenv:Header>
                <tem:Authentication xmlns:tem="http://tempuri.org/">
                    <biz:Database xmlns:biz="http://schemas.datacontract.org/2004/07/Bizzio.Srv.Extensions.RiznShop">{self.auth["DATABASE"]}</biz:Database>
                    <biz:Username xmlns:biz="http://schemas.datacontract.org/2004/07/Bizzio.Srv.Extensions.RiznShop">{self.auth["USERNAME"]}</biz:Username>
                   <biz:Password xmlns:biz="http://schemas.datacontract.org/2004/07/Bizzio.Srv.Extensions.RiznShop">{self.auth["PASSWORD"]}</biz:Password>
                </tem:Authentication>
            </soapenv:Header>
            <soapenv:Body>
                <tem:GetArticlesRequest>
                    <tem:AvailableOnly>false</tem:AvailableOnly>
                     
                    {f'<tem:ModifiedAfter>{modified_after}</tem:ModifiedAfter>' if modified_after else ''}
                    <tem:ID_Site>{self.auth["SITE_ID"]}</tem:ID_Site>
                    <tem:IsFiles>true</tem:IsFiles>
                </tem:GetArticlesRequest>
            </soapenv:Body>
        </soapenv:Envelope>
        """
        headers = {
            "Content-Type": "text/xml",
            "charset": "utf-8",
            "SOAPAction": "http://tempuri.org/IRiznShopExtService/GetArticles"
        }
        
        try:
            response = requests.post(f"{self.base_url}", data=payload, headers=headers)
            print(f"🟢 Получен отговор от Bizzio: {response.status_code}")
            """ Запис на заявката в XML файл за проверка на съдържанието """
            with open("bizzio_request.xml", "wb") as f:
                f.write(payload.encode())
            print("📂 Записан XML файл: bizzio_request.xml")

            """ Запис на отговора в XML файл за проверка на съдържанието """
            with open("bizzio_response.xml", "wb") as f:
                f.write(response.content)
            print("📂 Записан XML файл: bizzio_response.xml")
            
            # Ако отговорът е твърде голям, записваме в XML файл
            if len(response.content) > 5 * 1024 * 1024:  # 5MB
                with open("bizzio_response.xml", "wb") as f:
                    f.write(response.content)
                print("📂 Записан голям XML файл: bizzio_response.xml")
                return "bizzio_response.xml"
            else:
                return response.text

        except requests.exceptions.RequestException as e:
            print(f"🔴 Грешка при връзка с Bizzio API: {e}")
            return None
