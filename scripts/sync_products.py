import sys
import os

# Добавяне на кореновата директория в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.product_sync import sync_products
from modules.product_sync import sync_products_batch

print("📡 Стартиране на синхронизацията...")
sync_products_batch()
print("✅ Синхронизация завършена!")
