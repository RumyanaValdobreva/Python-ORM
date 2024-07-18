from django.db import models


class ProductManager(models.Manager):
    def available_products(self):
        return self.filter(is_available=True)

    def available_products_in_category(self, category_name: str):
        return self.filter(category__name=category_name, is_available=True)