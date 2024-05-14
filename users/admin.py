from django.contrib import admin
from .models import Department,Student,Company,AppliedCandidates,JobPosting

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'date_of_birth', 'email', 'department', 'cgpa', 'cv','photo']  
    search_fields = ['name', 'email'] 
    list_filter = ['department']  

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_id','company_name', 'location', 'establishment_year','industry_type']  
    search_fields = ['company_id','company_name', 'location'] 
    list_filter = ['industry_type']
     
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['company_id','job_title', 'job_requirement', 'job_type', 'job_package', 'last_date']
    search_fields = ['company_id','job_title', 'job_type'] 
    list_filter = ['job_type', 'job_package'] 

class AppliedCandidatesAdmin(admin.ModelAdmin):
     list_display = ('student', 'job_posting') 

admin.site.register(Department)
admin.site.register(JobPosting,JobPostingAdmin)
admin.site.register(AppliedCandidates,AppliedCandidatesAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Student, StudentAdmin)
