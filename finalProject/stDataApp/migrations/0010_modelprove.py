# Generated by Django 5.0.1 on 2024-02-18 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stDataApp", "0009_delete_rawdata"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModelProve",
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
                (
                    "sector_standard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="stDataApp.sectorstandards",
                    ),
                ),
            ],
        ),
    ]