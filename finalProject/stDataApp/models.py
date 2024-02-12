from django.db import models



class SectorStandards(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255, null=False)
    sector_standard = models.CharField(max_length=255, null=True)
    sector_label = models.TextField()

    def __str__(self):
        return f"ID: {self.id}, Code: {self.code}, Standard: {self.sector_standard}, Label: {self.sector_label}"
    
    
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    country_code_2 = models.CharField(max_length=2)
    country_code_3 = models.CharField(max_length=3)

    def __str__(self):
        return self.name

class Company(models.Model):
    company_id = models.CharField(max_length=100)
    company_national_id = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    company_country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    company_sector_standard = models.ForeignKey(SectorStandards, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.company_name