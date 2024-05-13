from django.contrib import admin
from .models import Department,Student,Company

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'date_of_birth', 'email', 'department', 'cgpa', 'cv','photo']  
    search_fields = ['name', 'email'] 
    list_filter = ['department']  

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'location', 'establishment_year','industry_type']  
    search_fields = ['company_name', 'location'] 
    list_filter = ['industry_type'] 

admin.site.register(Department)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Student, StudentAdmin)
