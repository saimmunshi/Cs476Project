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
from django.contrib.auth import get_user_model
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
        print("--- DEBUG: POST REQUEST RECEIVED ---")
        
        # 1. Print all data received
        print(f"Data: {request.POST}")
        
        # 2. Check for file
        image_url = None
        image_file = request.FILES.get('UploadPFP')
        if image_file:
            print(f"--- DEBUG: Image found: {image_file.name} ---")
            try:
                upload_result = cloudinary.uploader.upload(
                    image_file, 
                    folder="Mentora_Profiles"
                )
                image_url = upload_result.get('secure_url')
                print(f"--- DEBUG: Cloudinary Success: {image_url} ---")
            except Exception as e:
                print(f"--- DEBUG: Cloudinary Error: {e} ---")
        else:
            print("--- DEBUG: No image file provided ---")

        # 3. Validation Check
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        print(f"--- DEBUG: Creating User: {email} with Role: {role} ---")

        if User.objects.filter(email=email).exists():
            print("--- DEBUG: ERROR - User already exists ---")
            return render(request, 'student-registration.html', {'error': 'Email already exists'})

        try:
            # 4. Create User
            user = User.objects.create_user(
                username=request.POST.get('name'),  # Changed from email to name
                email=email, 
                password=password
            )
            print(f"--- DEBUG: User Created! ID: {user.id} ---")

            # 5. Create Profile
            if role == 'student':
                print("--- DEBUG: Attempting to create Student Profile ---")
                student = Student.objects.create(
                    user=user,
                    full_name=request.POST.get('name'),
                    student_id=request.POST.get('studentId'),
                    profile_image_url=image_url
                )
                print(f"--- DEBUG: Student Profile Created! ID: {student.id} ---")
                
            elif role == 'teacher':
                print("--- DEBUG: Attempting to create Teacher Profile ---")
                teacher = Teacher.objects.create(
                    user=user,
                    full_name=request.POST.get('name'),
                    license_number=request.POST.get('license'),
                    specialization=request.POST.get('specialization'),
                    profile_image_url=image_url
                )
                print(f"--- DEBUG: Teacher Profile Created! ID: {teacher.id} ---")
            
            # 6. Login
            #login(request, user)
            #print("--- DEBUG: User Logged In. Redirecting... ---")
            #return redirect('/')

        except Exception as e:
            print(f"--- CRITICAL ERROR DURING SAVE: {e} ---")
            return render(request, 'student-registration.html', {'error': str(e)})

    return render(request, 'student-registration.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user

        # CORRECTED CHECK for the student profile
        if hasattr(user, 'students_student_profile'):
            # The user has a student profile, redirect to their dashboard
            return reverse_lazy('student_dashboard')
        
        # CORRECTED CHECK for the teacher profile
        elif hasattr(user, 'teachers_teacher_profile'):
            # The user has a teacher profile, redirect them
            # (You can create a 'teacher-dashboard' URL later)
            return reverse_lazy('home') # Replace with 'teacher-dashboard' when ready
        
        # Fallback for other users (like superusers without profiles)
        else:
            return reverse_lazy('home')

def home(request):
    return render(request, 'home.html')