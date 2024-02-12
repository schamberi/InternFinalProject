# Generated by Django 5.0.1 on 2024-02-12 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stDataApp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("country_code_2", models.CharField(max_length=2)),
                ("country_code_3", models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name="Company",
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
                ("company_id", models.CharField(max_length=100)),
                ("company_national_id", models.CharField(max_length=100)),
                ("company_name", models.CharField(max_length=255)),
                (
                    "company_sector_standard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="stDataApp.sectorstandards",
                    ),
                ),
                (
                    "company_country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="stDataApp.country",
                    ),
                ),
            ],
        ),
    ]
