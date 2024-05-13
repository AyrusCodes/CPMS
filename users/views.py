from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Student,Company
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializers, CompanySerializers
from django.contrib.auth.models import User

class StudentUploadForm(APIView):
    def post(self, request):
        serializer = StudentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyUploadForm(APIView):
    def post(self, request):
        serializer = CompanySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        cgpa = request.POST.get('cgpa')
        cv = request.FILES.get('cv')  
        photo = request.FILES.get('photo')  
        new_student = Student(
            student_id=student_id,
            name=name,
            dob=dob,
            email=email,
            department=department,
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
    student_id = request.user.id
    student_data = Student.objects.get(id=student_id)
    context = {
        'student_data': student_data
    }
    return render(request, 'users/studdash.html',context)
