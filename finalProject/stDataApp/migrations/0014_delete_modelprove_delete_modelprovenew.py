# Generated by Django 5.0.1 on 2024-02-19 10:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stDataApp", "0013_modelprovenew"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ModelProve",
        ),
        migrations.DeleteModel(
            name="ModelProveNew",
        ),
    ]
