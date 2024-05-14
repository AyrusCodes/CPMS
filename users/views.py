from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import JobPosting, Student, Company, AppliedCandidates
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobSerializers, StudentSerializers, CompanySerializers, CandidateSerializers
from django.contrib.auth.models import User

class StudentUploadForm(APIView):
    def post(self, request):
        serializer = StudentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Student registered successfully!')
            return redirect('student_login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadCV(APIView):
    def post(self, request):
        try:
            username = request.user.username
            student = Student.objects.get(student_id=username)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializers(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            message = {'success': 'CV uploaded successfully!'}
            return redirect('stud_dashboard')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyUploadForm(APIView):
    def post(self, request):
        serializer = CompanySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Company registered successfully!')
            return redirect('company_login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CandidatesApply(APIView):
    def post(self, request):
        selected_jobs = request.data.get('selected_jobs', [])
        current_user = request.user
        for job_id in selected_jobs:
            try:
                job = JobPosting.objects.get(id=job_id)
                AppliedCandidates.objects.create(student=current_user, job_posting=job)
            except JobPosting.DoesNotExist:
                return Response({"error": "Job does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CandidateSerializers(data=request.data)
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

def stud_dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
        student = Student.objects.get(student_id=username)
        context = {'student': student}
        return render(request, 'users/studdash.html', context)
    else:
        return HttpResponse("Username not found in session")
    
def stud_apply_job(request):
    if request.method == 'POST':
        selected_jobs = request.POST.getlist('selected_jobs')
        current_user = request.user
        for job_id in selected_jobs:
            job = JobPosting.objects.get(id=job_id)
            AppliedCandidates.objects.create(student=current_user, job_posting=job)
        return redirect('stud_dashboard')
    else:
        job_postings = JobPosting.objects.all()
        job_postings_with_company_name = []
        for job in job_postings:
            company_name = Company.objects.get(company_id=job.company_id).company_name
            job_with_company_name = {
                'job': job,
                'company_name': company_name
            }
            print(job_with_company_name)
            job_postings_with_company_name.append(job_with_company_name)
        return render(request, 'users/applyjob.html', {'job_postings': job_postings_with_company_name})

    
def stud_results(request):
    return render(request, 'users/results.html')

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
        context = {'company': company}
        return render(request, 'users/comp_jobpost.html',context)
    
class ApplyPost(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            username = request.user.username
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        mutable_data = request.data.copy()
        mutable_data['company_id'] = username

        serializer = JobSerializers(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Job Posted successfully!')
            return redirect('comp_dashboard')        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def posted_jobs(request):
    if request.user.is_authenticated:
        username = request.user.username
        job_postings = JobPosting.objects.filter(company_id=username)
        return render(request, 'users/posted_jobs.html', {'job_postings': job_postings})