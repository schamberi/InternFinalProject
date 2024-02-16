from django.shortcuts import render
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# from .models import SectorStandards,Company,Country
from django.http import HttpResponse
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from stDataApp.models import SectorStandards,Company,Country,ExcelFile

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
        


class StandartData(APIView):
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
########################################  ca levizim qe duhet             
            # Find the column containing the word "code" or "label"
            # sector_column = None
            # for column in excel_data.columns:
            #     column_name = str(column).lower()
            #     if 'code' in column_name or 'label' in column_name or 'standard' in column_name:
            #         sector_column = column
            #         break

            # if sector_column is None:
            #     raise Exception("No column containing the word 'code' or 'label' found in the Excel data")
#################
            # Load the SectorStandards data
            # sector_standards = SectorStandards.objects.all()
            # sector_standard_names = [standard.sector_standard.lower() for standard in sector_standards]

            # # Calculate similarity using TF-IDF and cosine similarity
            # tfidf_vectorizer = TfidfVectorizer()
            # tfidf_matrix = tfidf_vectorizer.fit_transform(sector_standard_names)
            
            for index, row in excel_data.iterrows():
                company_id = row.get(row.filter(like='id').index[0])
                national_columns = row.filter(like='national').filter(like='id')
                company_national_id = national_columns.iat[0] if not national_columns.empty else None
                company_name = row.get(row.filter(like='name').index[0])
                #company_sector_value = row.get(sector_column)
                company_country_name = row.get(row.filter(like='country').index[0])
                #company_standard_name = row.get(sector_column)
                company_standard_name = row.get(next(filter(lambda x: 'code' in x or 'label' in x or 'standard' in x, row.index), None))


                company_standard_id = None
                for standard in SectorStandards.objects.all():
                    if (str(standard.sector_standard).lower() == str(company_standard_name).lower() or
                        company_standard_name.lower() == standard.code):
                        company_standard_id = standard.id
                        break

                if company_standard_id is None:
                    company_standard_id = None

                company_country_id = None
                for country in Country.objects.all():
                    if (country.name.lower() == company_country_name.lower() or
                        company_country_name.lower() == country.country_code_2.lower() or
                        company_country_name.lower() == country.country_code_3.lower()):
                        company_country_id = country.id
                        break

                if company_country_id is None:
                    company_country_id = None

                Company.objects.update_or_create(
                    company_id=company_id,
                    
                        company_national_id= company_national_id,
                        company_name= company_name,
                        company_sector_standard_id= company_standard_id,
                        company_country_id= company_country_id,
                        raw_data_id= raw_data_id
                    
                )

            return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
