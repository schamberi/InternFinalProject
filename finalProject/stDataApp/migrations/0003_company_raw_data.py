# Generated by Django 5.0.1 on 2024-02-14 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stDataApp", "0002_country_company"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="raw_data",
            field=models.JSONField(null=True),
        ),
    ]