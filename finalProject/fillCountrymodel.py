import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finalProject.settings")
django.setup()
from django.db import transaction
from stDataApp.models import Country

def create_countries():
    # Define data for countries
    country_data = [
        {"name": "United States", "country_code_2": "US", "country_code_3": "USA"},
        {"name": "Canada", "country_code_2": "CA", "country_code_3": "CAN"},
        {"name": "Mexico", "country_code_2": "MX", "country_code_3": "MEX"},
        {"name": "Argentina", "country_code_2": "AR", "country_code_3": "ARG"},
        {"name": "Brazil", "country_code_2": "BR", "country_code_3": "BRA"},
        {"name": "United Kingdom", "country_code_2": "GB", "country_code_3": "GBR"},
        {"name": "Germany", "country_code_2": "DE", "country_code_3": "DEU"},
        {"name": "France", "country_code_2": "FR", "country_code_3": "FRA"},
        {"name": "Italy", "country_code_2": "IT", "country_code_3": "ITA"},
        {"name": "Spain", "country_code_2": "ES", "country_code_3": "ESP"},
        {"name": "Netherlands", "country_code_2": "NL", "country_code_3": "NLD"},
        {"name": "Sweden", "country_code_2": "SE", "country_code_3": "SWE"},
        {"name": "Switzerland", "country_code_2": "CH", "country_code_3": "CHE"},
        {"name": "Norway", "country_code_2": "NO", "country_code_3": "NOR"},
        {"name": "Denmark", "country_code_2": "DK", "country_code_3": "DNK"},
        {"name": "Finland", "country_code_2": "FI", "country_code_3": "FIN"},
        {"name": "Greece", "country_code_2": "GR", "country_code_3": "GRC"},
        {"name": "Portugal", "country_code_2": "PT", "country_code_3": "PRT"},
        {"name": "Ireland", "country_code_2": "IE", "country_code_3": "IRL"},
        {"name": "Estonia", "country_code_2": "EE", "country_code_3": "EST"},
        {"name": "Belgium", "country_code_2": "BE", "country_code_3": "BEL"},
        {"name": "Austria", "country_code_2": "AT", "country_code_3": "AUT"},
        {"name": "Czech Republic", "country_code_2": "CZ", "country_code_3": "CZE"},
        {"name": "Hungary", "country_code_2": "HU", "country_code_3": "HUN"},
        {"name": "Poland", "country_code_2": "PL", "country_code_3": "POL"},
        {"name": "Slovakia", "country_code_2": "SK", "country_code_3": "SVK"},
        {"name": "Slovenia", "country_code_2": "SI", "country_code_3": "SVN"},
        {"name": "Bulgaria", "country_code_2": "BG", "country_code_3": "BGR"},
        {"name": "Romania", "country_code_2": "RO", "country_code_3": "ROU"},
        {"name": "Croatia", "country_code_2": "HR", "country_code_3": "HRV"},
        {"name": "Lithuania", "country_code_2": "LT", "country_code_3": "LTU"},
        {"name": "Latvia", "country_code_2": "LV", "country_code_3": "LVA"},
        {"name": "Luxembourg", "country_code_2": "LU", "country_code_3": "LUX"},
        {"name": "Malta", "country_code_2": "MT", "country_code_3": "MLT"},
        {"name": "Cyprus", "country_code_2": "CY", "country_code_3": "CYP"},
        {"name": "Iceland", "country_code_2": "IS", "country_code_3": "ISL"},
        {"name": "Liechtenstein", "country_code_2": "LI", "country_code_3": "LIE"},
        {"name": "Monaco", "country_code_2": "MC", "country_code_3": "MCO"},
        {"name": "San Marino", "country_code_2": "SM", "country_code_3": "SMR"},
        {"name": "Andorra", "country_code_2": "AD", "country_code_3": "AND"},
        {"name": "Vatican City", "country_code_2": "VA", "country_code_3": "VAT"},
        # Add more countries as needed
    ]

    # Bulk create countries
    with transaction.atomic():
        Country.objects.bulk_create([
        Country(**data) for data in country_data
        ])
