from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import JobPosting, Student,Company
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobSerializers, StudentSerializers, CompanySerializers
from django.contrib.auth.models import User

class StudentUploadForm(APIView):
    def post(self, request):
        serializer = StudentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Student registered successfully!')
            return redirect('student_login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyUploadForm(APIView):
    def post(self, request):
        serializer = CompanySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Company registered successfully!')
            return redirect('company_login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JobUploadForm(APIView):
    def post(self, request):
        serializer = JobSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def logout(request):
    return render(request, 'users/logout.html')

def student_reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('studreg_details')
    else:
        form = UserCreationForm()
    return render(request, 'users/stud_reg.html', {'form': form }) 

def studreg_details(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        department = request.POST.get('department')
        batch = request.POST.get('batch')
        cgpa = request.POST.get('cgpa')
        cv = request.FILES.get('cv')  
        photo = request.FILES.get('photo')  
        new_student = Student(
            student_id=student_id,
            name=name,
            dob=dob,
            email=email,
            department=department,
            batch=batch,
            cgpa=cgpa,
            cv=cv,
            photo=photo
        )
        new_student.save()
        messages.success(request,"Student registered successfully!")
        return redirect('student_login')
    else:
        return render(request, 'users/studregform.html')

def comp_reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('compreg_details')
    else:
        form = UserCreationForm()
    return render(request, 'users/comp_reg.html', {'form': form }) 

def compreg_details(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        establishment_year = request.POST.get('establishment_year')
        industry_type = request.POST.get('industry_type')
        
        # Create a new Company object and save it to the database
        new_company = Company.objects.create(
            company_name=company_name,
            location=location,
            establishment_year=establishment_year,
            industry_type=industry_type
        )
        messages.success(request, 'Company registered successfully!')
        return redirect('company_login')  # Redirect to a success page
    return render(request, 'users/compregform.html')

def stud_dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
        student = Student.objects.get(student_id=username)
        context = {'student': student}
        return render(request, 'users/studdash.html', context)
    else:
        return HttpResponse("Username not found in session")
    
def upload_cv(request):
    if request.method == 'POST' and request.FILES.get('cv'):
        cv_file = request.FILES['cv']
        student = request.user.username  # Assuming student is authenticated
        student.cv = cv_file
        student.save()
        messages.success(request, 'CV uploaded successfully!')
    return redirect('stud_dashboard')
    
def stud_apply_job(request):
    return render(request, 'users/applyjob.html')

def stud_results(request):
    return render(request, 'users/results.html')

def comp_dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
        company = Company.objects.get(company_id=username)
        context = {'company': company}
        return render(request, 'users/companydash.html', context)
    else:
        return HttpResponse("Username not found in session")
    
def apply_post(request):
    if request.user.is_authenticated:
        username = request.user.username
        company = Company.objects.get(company_id=username)
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        job_requirement = request.POST.get('job_requirement')
        job_type = request.POST.get('job_type')
        job_package = request.POST.get('job_package')
        last_date = request.POST.get('last_date')
        job_package = request.POST.get('job_package')
        
        new_job = JobPosting.objects.create(
            company_id = username,
            job_title=job_title,
            job_requirement=job_requirement,
            job_type=job_type,
            job_package=job_package,
            last_date=last_date
        )
        messages.success(request, 'Job Posted successfully!')
        return redirect('comp_dashboard')  # Redirect to a success page
    return render(request, 'users/comp_jobpost.html', {'company': company})

