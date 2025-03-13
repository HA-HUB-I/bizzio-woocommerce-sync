import requests
from config.settings import MEDIA_UPLOAD_URL, WOO_API

class ImageHandler:
    @staticmethod
    def upload_image(image_url):
        """Качва изображение в WordPress Media Library и връща ID"""
        if not image_url:
            return None

        image_name = image_url.split("/")[-1]
        headers = {
            "Authorization": f"Basic {WOO_API['CONSUMER_KEY']}:{WOO_API['CONSUMER_SECRET']}",
            "Content-Disposition": f"attachment; filename={image_name}"
        }

        response = requests.post(MEDIA_UPLOAD_URL, headers=headers, files={"file": requests.get(image_url).content})

        if response.status_code == 201:
            return response.json().get("id")
        else:
            print(f"🔴 Грешка при качване на изображение: {response.text}")
            return None
