from sqlite3 import IntegrityError
from django.shortcuts import render
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from stDataApp.models import SectorStandards,Company,Country,ExcelFile
from django.db.models import Q
from difflib import get_close_matches

###ProvaNdryshe

class TryStoringExcel(APIView):
    template_name = 'uploadButon.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')

        if not excel_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a new instance of ExcelFile model and save the uploaded file
            excel_file_obj = ExcelFile.objects.create(file=excel_file)

            return Response({'message': 'Excel file uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 ##### Shkarko filen excel       
class DownloadRawData(APIView):
    def get(self, request, file_id):
        excel_file = get_object_or_404(ExcelFile, pk=file_id)
        file_path = excel_file.file.path
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

class StandartDataMapping(APIView):
    template_name = 'uploadButon.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('excel_file')

        if not excel_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file into a pandas DataFrame
            excel_data = pd.read_excel(excel_file)
            
            excel_file_obj = ExcelFile.objects.create(file=excel_file)
            raw_data_id = excel_file_obj.pk
            
            companies_to_create = []
            sector_standard_ids = {}  # Initialize a dictionary to store matched sector standard IDs

            for index, row in excel_data.iterrows():
                company_id = row.get(row.filter(like='id').index[0])
                national_columns = row.filter(like='national').filter(like='id')
                company_national_id = national_columns.iat[0] if not national_columns.empty else None
                company_name = row.get(row.filter(like='name').index[0])
                company_country_name = row.get(row.filter(like='country').index[0])
                id_of_matched_sector_standard = None

                if any(excel_data.columns.str.contains('code')):
                    column_name = [col for col in excel_data.columns if 'code' in col][0]
                    values = row[column_name]  # Get the values in the specific row's column
                    if isinstance(values, (int, float)):  # Handle case when values is an int or float
                        values = [values]
                    for value in values:  # Iterate through the values
                        lower_value = str(value).lower()
                        sector_standard_match = SectorStandards.objects.filter(
                            Q(code=lower_value) | Q(code__iexact=lower_value.lstrip('0'))
                        ).first()
                        if sector_standard_match:
                            id_of_matched_sector_standard = sector_standard_match.id
                            sector_standard_ids[index] = id_of_matched_sector_standard  # Store the ID in the dictionary
                            break
                elif any(excel_data.columns.str.contains('standard')):
                    column_name = [col for col in excel_data.columns if 'standard' in col][0]
                    values = row[column_name]  # Get the values in the specific row's column

                    if isinstance(values, str):  # Check if values is a single string, convert to list if necessary
                        values = [values]
                        
                    for value in values:  # Iterate through the values
                        lower_value = value.lower()
                        # Tokenize the value into individual words or phrases
                        tokens = lower_value.split()
                        # Look for similar matches in the database
                        matches = []
                        for token in tokens:
                            similar_matches = SectorStandards.objects.filter(sector_label__icontains=token)
                            matches.extend(similar_matches)
                        # Get the best match using a similarity algorithm
                        best_match = get_close_matches(lower_value, [match.sector_label.lower() for match in matches], n=1, cutoff=0.8)
                        if best_match:
                            sector_standard_match = SectorStandards.objects.filter(sector_label__iexact=best_match[0]).first()
                            if sector_standard_match:
                                id_of_matched_sector_standard = sector_standard_match.id
                                sector_standard_ids[index] = id_of_matched_sector_standard  # Store the ID in the dictionary
                                break

                company_country_id = None
                for country in Country.objects.all():
                    if (country.name.lower() == company_country_name.lower() or
                        company_country_name.lower() == country.country_code_2.lower() or
                        company_country_name.lower() == country.country_code_3.lower()):
                        company_country_id = country.id
                        break

                if company_country_id is None:
                    company_country_id = None

                company = Company(
                    company_id=company_id,
                    company_national_id=company_national_id,
                    company_name=company_name,
                    company_sector_standard_id=sector_standard_ids.get(index),  # Get the ID using the index
                    company_country_id=company_country_id,
                    raw_data_id=raw_data_id
                )
                companies_to_create.append(company)

            # Bulk create the companies
            Company.objects.bulk_create(companies_to_create)

            return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error': 'Integrity error - {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





