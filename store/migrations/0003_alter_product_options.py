# Generated by Django 5.0.2 on 2024-02-12 16:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_rename_image_product_images"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "product", "verbose_name_plural": "products"},
        ),
    ]
