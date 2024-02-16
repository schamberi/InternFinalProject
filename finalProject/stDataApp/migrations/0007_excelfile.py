# Generated by Django 5.0.1 on 2024-02-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stDataApp", "0006_alter_company_company_country_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExcelFile",
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
                ("file", models.FileField(upload_to="excel_files/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]