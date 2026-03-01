from django.shortcuts import render, redirect
import cloudinary
import cloudinary.uploader
from django.contrib import messages
from pathlib import Path
from datetime import datetime
from django.urls import reverse_lazy
from students.models import Student
from teachers.models import Teacher
from .models import CustomUser
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView

# Create your views here.

def home_view(request):
    return render(request, "home.html")

def teacher_register_view(request):
    return render(request, "teacher-registration.html")


"""
Author: Saim Munshi
Function Name: student_register_view
Purpose: direct view.py django to the correct html file
Update: Fixed Cloudinary-MongoDB picture upload - Mark
"""
# Get the active User model (CustomUser)
User = get_user_model()

def student_register_view(request):
    if request.method == 'POST':
        # Print all data received - Used to debug and test if POST data is being sent.
        print(f"Data: {request.POST}")
        
        # Check for file
        image_url = None
        image_file = request.FILES.get('UploadPFP')
        if image_file:
            try:
                upload_result = cloudinary.uploader.upload(
                    image_file, 
                    folder="Mentora_Profiles"
                )
                image_url = upload_result.get('secure_url')
                print(f"Student Register: Cloudinary Success: {image_url} ---")
            except Exception as e:
                print(f"Student Register: Cloudinary Error: {e} ---")
        else:
            print("Student Register: No image file provided")

        # Set user data with POST data
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(email=email).exists():
            print("Student Register: User already exists ---")
            return render(request, 'student-registration.html', {'error': 'Email already exists'})

        try:
            # Create User
            user = User.objects.create_user(
                username=request.POST.get('name'),  # Changed from email to name
                email=email, 
                password=password
            )

            # Create Profile - Student or Teacher
            if role == 'student':
                student = Student.objects.create(
                    user=user,
                    full_name=request.POST.get('name'),
                    student_id=request.POST.get('studentId'),
                    profile_image_url=image_url
                )
                
            elif role == 'teacher':
                teacher = Teacher.objects.create(
                    user=user,
                    full_name=request.POST.get('name'),
                    license_number=request.POST.get('license'),
                    specialization=request.POST.get('specialization'),
                    profile_image_url=image_url
                )
            
            # Auto Login
            login(request, user)
            if role == 'student':
                return redirect('student_dashboard') # Note: url names use underscore. See student/urls.py
            elif role == 'teacher':
                return redirect('home')  # replace with 'teacher_dashboard' when ready

        except Exception as e:
            print(f"--- CRITICAL ERROR DURING SAVE: {e} ---")
            return render(request, 'student-registration.html', {'error': str(e)})

    return render(request, 'student-registration.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user

        # Check for the student profile
        if hasattr(user, 'students_student_profile'):
            # The user has a student profile, redirect to their dashboard
            return reverse_lazy('student_dashboard')
        
        # Check for the teacher profile
        elif hasattr(user, 'teachers_teacher_profile'):
            # The user has a teacher profile, redirect them
            return reverse_lazy('home') # Note: Replace with 'teacher-dashboard' when ready
        
        # Fallback for other users (like superusers without profiles)
        else:
            return reverse_lazy('home')


def Feedback(request):  
    #Added by Matthew/Spooky so when called returns index.html.
    return render(request, 'index.html')