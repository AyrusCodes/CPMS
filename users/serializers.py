from rest_framework import serializers
from.models import Student,Company,JobPosting

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'date_of_birth', 'email', 'department', 'batch' 'cgpa', 'cv', 'photo']

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_id','company_name', 'location', 'establishment_year', 'industry_type']

class JobSerializers(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['company_id','job_title', 'job_requirement', 'job_type', 'job_package', 'last_date']