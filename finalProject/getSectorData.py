import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finalProject.settings")
django.setup()
import pandas as pd
from stDataApp.models import SectorStandards

def fill_sector_standards_from_excel():
    try:
        # Path to the Excel file
        excel_file_path = r'C:\\Users\\scham\\Desktop\\InternFinalProject\\finalProject\\StaticData\\sector_nace_naics.xlsx'

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file_path)

        # Filter rows where sector_standard is either "NACE" or "NAICS"
        filtered_rows = df[(df['sector_standard'] == 'NACE') | (df['sector_standard'] == 'NAICS')]

        # Create a list to store SectorStandards objects
        sector_standards_list = []

        # Iterate over filtered rows and append objects to the list
        for index, row in filtered_rows.iterrows():
            # Stripping leading zeros from the code column
            code = str(row['code']).lstrip('0')
            sector_standard_obj = SectorStandards(
                code=code,
                sector_standard=row['sector_standard'],
                sector_label=row['sector_label']
            )
            sector_standards_list.append(sector_standard_obj)

        # Use bulk_create to create objects in bulk
        SectorStandards.objects.bulk_create(sector_standards_list)

        print("Data from Excel file has been successfully stored in the SectorStandards model.")

    except FileNotFoundError:
        print("Excel file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Call the function to fill sector standards from Excel
fill_sector_standards_from_excel()
