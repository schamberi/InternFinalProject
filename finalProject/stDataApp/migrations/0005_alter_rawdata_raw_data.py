# Generated by Django 5.0.1 on 2024-02-14 12:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stDataApp", "0004_rawdata_alter_company_raw_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rawdata",
            name="raw_data",
            field=models.JSONField(null=True),
        ),
    ]
