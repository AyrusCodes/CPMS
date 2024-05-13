from rest_framework import serializers
from.models import Student,Company

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'date_of_birth', 'email', 'department', 'cgpa', 'cv','photo']

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'location', 'establishment_year', 'industry_type']