from django.shortcuts import render
import pandas as pd
from openpyxl import load_workbook
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import SectorStandards,Company,RawData,Country
from django.shortcuts import render
from .serializers import RawDataSerializer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from stDataApp.models import SectorStandards,Company,RawData,Country
# class ExcelUpload(APIView):
#     template_name = 'uploadButon.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         excel_file = request.FILES.get('excel_file')

#         if not excel_file:
#             return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Read the Excel file into a pandas DataFrame
#             excel_data = pd.read_excel(excel_file)

#             # Create a list to store the company objects to be bulk created
#             companies_to_create = []

#             # Determine the column name containing country data
#             country_column_name = None
#             for column_name in excel_data.columns:
#                 if 'country' in column_name.lower():
#                     country_column_name = column_name
#                     break
                

#             if not country_column_name:
#                 return Response({'error': 'No suitable column found for country data'}, status=status.HTTP_400_BAD_REQUEST)
            
            
#             sector_data_column_name = None
#             for column_name in excel_data.columns:
#                 if ('code' in column_name.lower() or 'label' in column_name.lower()):
#                    sector_data_column_name = column_name
#                    break

#             if not sector_data_column_name:
#                 return Response({'error': 'No suitable column found for sector data'}, status=status.HTTP_400_BAD_REQUEST)
            

#             # Iterate through the rows of the DataFrame
#             for index, row in excel_data.iterrows():
#                 # Extract data from the current row
#                 company_id = row['company_id']
#                 company_national_id = row['company_national_id']
#                 company_name = row['company_name']
#                 sector_data = row[sector_data_column_name]  # Assuming this column contains either code or sector_label
#                 country_name = row[country_column_name]  # Retrieve country name from the dynamically selected column

#                 # Extract raw data from the row
#                 raw_data_dict = {column: row[column] for column in excel_data.columns}

#                 # Create a RawData object to store the dictionary
#                 raw_data_object = RawData.objects.create(raw_data=raw_data_dict)

#                 # Check if the sector_data matches code or sector_label
#                 sector_standard = None
#                 if 'label' in row:
#                     sector_standard = SectorStandards.objects.filter(sector_label=sector_data).first()
#                 elif 'code' in row:
#                     sector_standard = SectorStandards.objects.filter(code=sector_data).first()

#                 if not sector_standard:
#                     # If the code doesn't match, try to find a similar sector_label
#                     similar_standards = SectorStandards.objects.all()
#                     best_match = None
#                     best_similarity = 0
#                     for standard in similar_standards:
#                         similarity = jellyfish.jaro_winkler(sector_data, standard.sector_label)
#                         if similarity > best_similarity:
#                             best_similarity = similarity
#                             best_match = standard

#                     sector_standard = best_match

#                 # Find the corresponding country
#                 country = Country.objects.filter(name__iexact=country_name).first()
#                 if not country:
#                     return Response({'error': f"Country '{country_name}' not found in the database"}, status=status.HTTP_400_BAD_REQUEST)

#                 # Create a dictionary representing the company data
#                 company_data = {
#                     'company_id': company_id,
#                     'company_national_id': company_national_id,
#                     'company_name': company_name,
#                     'company_country_id': country.id,
#                     'company_sector_standard_id': sector_standard.id if sector_standard else None,
#                     'raw_data': raw_data_object.id  # Storing the pk reference of the RawData object
#                 }
#                 companies_to_create.append(Company(**company_data))

#             # Bulk create the company objects
#             Company.objects.bulk_create(companies_to_create)

#             return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


##################
#API to retrieve
class RawUpload(APIView):
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

            # Create a list to store the raw data dictionaries
            raw_data_list = []

            # Convert each row to a dictionary and append to the list
            for index, row in excel_data.iterrows():
                raw_data_dict = row.to_dict()
                raw_data_list.append(raw_data_dict)

            # Create a RawData object to store the dictionary
            raw_data_object = RawData.objects.create(raw_data=raw_data_list)

            return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


###Marrim te dhenat qe futem 
            

class RawDataAPI(APIView):
    def get(self, request, format=None):
        try:
            # Retrieve all instances of RawData from the database
            raw_data_instances = RawData.objects.all()

            # Serialize the raw data instances
            serializer = RawDataSerializer(raw_data_instances, many=True)

            # Return serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#Standardized Data
































class Prova(APIView):
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

            # Find the column containing the word "code" or "label"
            sector_column = None
            for column in excel_data.columns:
                column_name = str(column)
                if 'code' in column_name.lower() or 'label' in column_name.lower():
                    sector_column = column
                    break

            if sector_column is None:
                raise Exception("No column containing the word 'code' or 'label' found in the Excel data")

            # Load the SectorStandards data
            sector_standards = SectorStandards.objects.all()
            sector_standard_names = [standard.sector_standard for standard in sector_standards]

            # Calculate similarity using TF-IDF and cosine similarity
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(sector_standard_names)
            
            # Convert the DataFrame to a list of dictionaries
            raw_data_list = []
            for index, row in excel_data.iterrows():
                raw_data_dict = row.to_dict()
                raw_data_list.append(raw_data_dict)

            # Create a RawData object to store the dictionary
            raw_data_object = RawData.objects.create(raw_data=raw_data_list)
            raw_data_id = raw_data_object.pk

            # Assuming excel_data is a pandas DataFrame with your Excel data
            for index, row in excel_data.iterrows():
                company_id = row.get(row.filter(like='id').index[0])
                national_columns = row.filter(like='national').filter(like='id')
                company_national_id = national_columns.iat[0] if not national_columns.empty else None
                company_name = row.get(row.filter(like='name').index[0])
                company_sector_value = row.get(sector_column)

                # Calculate similarity between the company sector value and sector standards
                sector_tfidf = tfidf_vectorizer.transform([str(company_sector_value)])
                cosine_similarities = cosine_similarity(sector_tfidf, tfidf_matrix).flatten()
                best_match_index = cosine_similarities.argmax()
                best_match_score = cosine_similarities[best_match_index]

                if best_match_score > 0.8:  # Threshold for similarity
                    company_sector_standard = sector_standards[best_match_index]
                else:
                    # Handle case when similarity is low
                    company_sector_standard = None

                # Create or update Company object based on data
                company, created = Company.objects.update_or_create(
                    company_id=company_id,  # If 'company_id' is the field name for your company's primary key
                    
                    company_national_id= company_national_id,
                    company_name=company_name,
                    company_sector_standard= company_sector_standard or None,
                    raw_data_id=raw_data_id
                
                )

            return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














class ProvaDyte(APIView):
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

            # Find the column containing the word "code" or "label"
            sector_column = None
            for column in excel_data.columns:
                column_name = str(column)
                if 'code' in column_name.lower() or 'label' in column_name.lower() or 'standard' in column_name.lower():
                    sector_column = column
                    break

            if sector_column is None:
                raise Exception("No column containing the word 'code' or 'label' found in the Excel data")

            # Load the SectorStandards data
            sector_standards = SectorStandards.objects.all()
            sector_standard_names = [standard.sector_standard for standard in sector_standards]

            # Calculate similarity using TF-IDF and cosine similarity
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(sector_standard_names)
            
            # Convert the DataFrame to a list of dictionaries
            raw_data_list = []
            for index, row in excel_data.iterrows():
                raw_data_dict = row.to_dict()
                raw_data_list.append(raw_data_dict)

            # Create a RawData object to store the dictionary
            raw_data_object = RawData.objects.create(raw_data=raw_data_list)
            raw_data_id = raw_data_object.pk

            # Assuming excel_data is a pandas DataFrame with your Excel data
            for index, row in excel_data.iterrows():
                company_id = row.get(row.filter(like='id').index[0])
                national_columns = row.filter(like='national').filter(like='id')
                company_national_id = national_columns.iat[0] if not national_columns.empty else None
                company_name = row.get(row.filter(like='name').index[0])
                company_sector_value = row.get(sector_column)
                company_country_name = row.get(row.filter(like='country').index[0])

                # Calculate similarity between the company sector value and sector standards
                sector_tfidf = tfidf_vectorizer.transform([str(company_sector_value)])
                cosine_similarities = cosine_similarity(sector_tfidf, tfidf_matrix).flatten()
                best_match_index = cosine_similarities.argmax()
                best_match_score = cosine_similarities[best_match_index]

                if best_match_score > 0.8:  # Threshold for similarity
                    company_sector_standard = sector_standards[best_match_index]
                else:
                    # Handle case when similarity is low
                    company_sector_standard = None

                # Find the corresponding Country object or create a new one if not found
                company_country_id = None
                for country in Country.objects.all():
                    if (country.name.lower() == company_country_name.lower() or
                     company_country_name.lower() == country.country_code_2.lower() or
                     company_country_name.lower() == country.country_code_3.lower()):
                        company_country_id = country.id
                        break

                if company_country_id is None:
                    rcompany_country_id = None

                # Create or update Company object based on data
                company, created = Company.objects.update_or_create(
                    company_id=company_id,  # If 'company_id' is the field name for your company's primary key
                    
                    company_national_id= company_national_id,
                    company_name= company_name,
                    company_sector_standard= company_sector_standard,
                    company_country_id=company_country_id,
                    raw_data_id=raw_data_id
                    
                )

            return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
        
        
        
class ProvaTrete(APIView):
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

            # Find the column containing the word "code" or "label"
            sector_column = None
            for column in excel_data.columns:
                column_name = str(column)
                if 'code' in column_name.lower() or 'label' in column_name.lower() or 'standard' in column_name.lower():
                    sector_column = column
                    break

            if sector_column is None:
                raise Exception("No column containing the word 'code' or 'label' found in the Excel data")

            # Load the SectorStandards data
            sector_standards = SectorStandards.objects.all()
            sector_standard_names = [standard.sector_standard for standard in sector_standards]

            # Calculate similarity using TF-IDF and cosine similarity
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(sector_standard_names)
            
            # Convert the DataFrame to a list of dictionaries
            raw_data_list = []
            for index, row in excel_data.iterrows():
                raw_data_dict = row.to_dict()
                raw_data_list.append(raw_data_dict)

            # Create a RawData object to store the dictionary
            raw_data_object = RawData.objects.create(raw_data=raw_data_list)
            raw_data_id = raw_data_object.pk

            # Assuming excel_data is a pandas DataFrame with your Excel data
            for index, row in excel_data.iterrows():
                company_id = row.get(row.filter(like='id').index[0])
                national_columns = row.filter(like='national').filter(like='id')
                company_national_id = national_columns.iat[0] if not national_columns.empty else None
                company_name = row.get(row.filter(like='name').index[0])
                company_sector_value = row.get(sector_column)
                company_country_name = row.get(row.filter(like='country').index[0])

                sector_match = None
                for standard in sector_standards:
                    standard_code_lower = str(standard.code).lower() if standard.code else ""
                    standard_label_lower = str(standard.sector_label).lower() if standard.sector_label else ""
                    if (str(company_sector_value).lower() == standard_code_lower or
                       str(company_sector_value).lower() == standard_label_lower):
                       sector_match = standard.id
                       break

                
                if sector_match is None:
                    sector_match=None
                
                #     sector_tfidf = tfidf_vectorizer.transform([str(company_sector_value)])
                #     cosine_similarities = cosine_similarity(sector_tfidf, tfidf_matrix).flatten()
                #     best_match_index = cosine_similarities.argmax()
                #     best_match_score = cosine_similarities[best_match_index]

                #     if best_match_score > 0.8:  
                #         sector_match = sector_standards[best_match_index].id

                
                # company_sector_standard = sector_match if sector_match else None

                # Find the corresponding Country object or create a new one if not found
                company_country_id = None
                for country in Country.objects.all():
                    if (country.name.lower() == company_country_name.lower() or
                        company_country_name.lower() == country.country_code_2.lower() or
                        company_country_name.lower() == country.country_code_3.lower()):
                        company_country_id = country.id
                        break

                # If no match is found, set company_country_id to None
                if company_country_id is None:
                    company_country_id = None

                # Create or update Company object based on data
                company, created = Company.objects.update_or_create(
                    company_id=company_id,  # If 'company_id' is the field name for your company's primary key
                    company_national_id= company_national_id,
                    company_name= company_name,
                    company_sector_standard_id= sector_match,
                    company_country_id=company_country_id,
                    raw_data_id=raw_data_id
                )

            return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
