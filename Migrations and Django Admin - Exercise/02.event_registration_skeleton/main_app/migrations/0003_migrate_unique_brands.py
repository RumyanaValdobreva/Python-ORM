# Generated by Django 5.0.4 on 2024-06-29 18:31

from django.db import migrations


def unique_brand_names(apps, schema_editor):
    shoes = apps.get_model('main_app', 'Shoe')
    unique_brands = apps.get_model('main_app', 'UniqueBrands')

    unique_brand = shoes.objects.values_list('brand', flat=True).distinct()

    for brand in unique_brand:
        unique_brands.objects.create(brand=brand)


def reverse_unique_brand_names(apps, schema_editor):
    unique_brands = apps.get_model('main_app', 'UniqueBrands')

    unique_brands.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [
        migrations.RunPython(unique_brand_names, reverse_unique_brand_names)
    ]
