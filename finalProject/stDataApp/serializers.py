from rest_framework import serializers
from .models import SectorStandards, Country, Company

class SectorStandardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorStandards
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
