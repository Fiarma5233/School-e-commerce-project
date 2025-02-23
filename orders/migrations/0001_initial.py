# Generated by Django 5.0.2 on 2024-02-15 12:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("store", "0004_variation"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order_number", models.CharField(max_length=30)),
                ("nom", models.CharField(max_length=50)),
                ("prenom", models.CharField(max_length=50)),
                ("phone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=50)),
                ("address_line_1", models.CharField(max_length=50)),
                ("address_line_2", models.CharField(blank=True, max_length=50)),
                ("country", models.CharField(max_length=50)),
                ("state", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("order_note", models.CharField(blank=True, max_length=100)),
                ("order_total", models.FloatField()),
                ("tax", models.FloatField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("Accepted", "Accepted"),
                            ("Completed", "Completed"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="New",
                        max_length=10,
                    ),
                ),
                ("ip", models.CharField(blank=True, max_length=20)),
                ("is_ordered", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_id", models.CharField(max_length=100)),
                ("payment_method", models.CharField(max_length=100)),
                ("amount_paid", models.CharField(max_length=100)),
                ("status", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("product_price", models.FloatField()),
                ("ordered", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orders.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "variations",
                    models.ManyToManyField(blank=True, to="store.variation"),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="orders.payment",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="orders.payment",
            ),
        ),
    ]
