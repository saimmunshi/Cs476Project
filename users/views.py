from django.shortcuts import render, redirect
import cloudinary
import cloudinary.uploader
from django.contrib import messages
from django.urls import reverse_lazy
from students.models import Student
from teachers.models import Teacher
from .models import CustomUser
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.views import LoginView
import re
# from django.contrib.auth import get_user_model
# from django.contrib.auth import authenticate, login
# from teachers.models import Teacher
# from django.contrib.auth.models import update_last_login
# from django.contrib.auth.signals import user_logged_in

# Create your views here.

def home_view(request):
    # Added by Matthew/Spooky: Render the generic home page.
    return render(request, "home.html")


"""
Author: Saim Munshi
Function Name: student_register_view
Purpose: direct view.py django to the correct html file
Update: Fixed Cloudinary-MongoDB picture upload - Mark
"""
# Added by Matthew/Spooky: Get the active User model (CustomUser).
User = get_user_model()

def main_page_view(request):
    # Added by Matthew/Spooky: Render the main landing page for authenticated users.
    return render(request, 'MainHome.html')


"""
Author: Saim Munshi
Function Name: student_register_view
Purpose: direct view.py django to the correct html file
Update: Fixed Cloudinary-MongoDB picture upload - Mark
"""
def student_register_view(request):
    # Added by Matthew/Spooky: Handle student registration form submission.
    if request.method == 'POST':
        # Added by Matthew/Spooky:Print all data received. Used to debug and test if POST data is being sent.
        print(f"Data: {request.POST}")
        
        # Added by Matthew/Spooky: Initialize image URL for Cloudinary upload.
        image_url = None
        image_file = request.FILES.get('UploadPFP')
        if image_file:
            try:
                # Added by Matthew/Spooky: Upload the profile picture to Cloudinary.
                upload_result = cloudinary.uploader.upload(
                    image_file, 
                    folder="Mentora_Profiles"
                )
                image_url = upload_result.get('secure_url')
                print(f"Student Register: Cloudinary Success: {image_url} ---")
            except Exception as e:
                # Added by Matthew/Spooky: Handle upload errors.
                print(f"Student Register: Cloudinary Error: {e} ---")
        else:
            print("Student Register: No image file provided")

        # Added by Matthew/Spooky:Set user data with POST data.
        email = request.POST.get('email')
        password = request.POST.get('mainpassword')
        confirmpassword = request.POST.get('confirmpassword')
        name = request.POST.get("name", "").strip()

        # Added by Matthew/Spooky: Regex to ensure full name format.
        name_regex = r"^[A-Za-z]+(?: [A-Za-z'-]+)+$"
        if not name: 
            messages.error(request, "Full name is required.")
            return render(request, "StudentRegistration.html")
        
        if not re.match(name_regex, name):
            messages.error(request, "Full name is Required")
            return render(request, "StudentRegistration.html")

        if User.objects.filter(email=email).exists():
            print("Student Register: User already exists ---")
            return render(request, 'StudentRegistration.html', {'error': 'Email already exists'})
        
        # Added by Matthew/Spooky: Password authentication.
        if password != confirmpassword:
            messages.error(request, "Password do not match.")
            return render(request, "StudentRegistration.html")
        
        try:
            user = User.objects.create_user(
                username=email,
                email=email, 
                password=password
            )

            # Added by Matthew/Spooky: Create Student profile linked to user.
            student = Student.objects.create(
                user=user,
                full_name=request.POST.get('name'),
                student_id=request.POST.get('studentId'),
                profile_image_url=image_url
            )
            
            # Added by Matthew/Spooky: Login.
            login(request, user)
            return redirect('signin_page_view')
        

        except Exception as e:
            print(f"--- CRITICAL ERROR DURING SAVE: {e} ---")
            return render(request, 'StudentRegistration.html', {'error': str(e)})

    # Added by Matthew/Spooky: Render the registration page for GET request.
    return render(request, 'StudentRegistration.html')


def teacher_register_view(request):
    # Added by Matthew/Spooky: Handle teacher registration form submission.
    if request.method == 'POST':
        # Added by Matthew/Spooky: Print all data received. Used to debug and test if POST data is being sent.
        print(f"Data: {request.POST}")
        
        # Added by Matthew/Spooky: Initialize image URL for Cloudinary upload.
        image_url = None
        image_file = request.FILES.get('UploadPFP')
        if image_file:
            try:
                # Added by Matthew/Spooky: Upload teacher profile image to Cloudinary.
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

        # Added by Matthew/Spooky: Set user data with POST data.
        email = request.POST.get('email')
        password = request.POST.get('mainpassword')
        confirmpassword = request.POST.get('confirmpassword')
        name = request.POST.get("name", "").strip()

        # Added by Matthew/Spooky: Regex to ensure full name.
        name_regex = r"^[A-Za-z]+(?: [A-Za-z'-]+)+$"
        if not name: 
            messages.error(request, "Full name is required.")
            return render(request, "TeacherRegistration.html")
        
        if not re.match(name_regex, name):
            messages.error(request, "Full name is Required")
            return render(request, "TeacherRegistration.html")
        if User.objects.filter(email=email).exists():
            print("Teacher Register: User already exists ---")
            return render(request, 'TeacherRegistration.html', {'error': 'Email already exists'})
        # Added by Matthew/Spooky: Password authentication.
        if password != confirmpassword:
            messages.error(request, "Password do not match.")
            return render(request, "TeacherRegistration.html")

        try:
            user = User.objects.create_user(
                username=email,
                email=email, 
                password=password
            )

            # Added by Matthew/Spooky: Create Teacher profile linked to user.
            teacher = Teacher.objects.create(
                user=user,
                full_name=request.POST.get('name'),
                license_number=request.POST.get('license'),
                specialization=request.POST.get('specialization'),
                profile_image_url=image_url
            )
            
            # Added by Matthew/Spooky: Login.
            login(request, user)
            return redirect('signin_page_view')

        except Exception as e:
            print(f"--- CRITICAL ERROR DURING SAVE: {e} ---")
            return render(request, 'TeacherRegistration.html', {'error': str(e)})

    # Added by Matthew/Spooky: Render the teacher registration page on GET.
    return render(request, 'TeacherRegistration.html')


"""Added By Mark: For redirecs """

class CustomLoginView(LoginView):
    template_name = 'StudentHomePage.html'

    def get_success_url(self):
        user = self.request.user

        # Added by Matthew/Spooky: Check if the user has a student profile.
        if hasattr(user, 'students_student_profile'):
            # Added by Matthew/Spooky: The user has a student profile, redirect to their dashboard.
            return reverse_lazy('student_home')
        
        # Added by Matthew/Spooky: Check if the user has a teacher profile.
        elif hasattr(user, 'teachers_teacher_profile'):
            # The user has a teacher profile, redirect them.
            return reverse_lazy('teacher_home') 
        
        # Added by Matthew/Spooky: Fallback for other users just in case.
        else:
            return reverse_lazy('signin_page_view')


def signin_page_view(request):
    # Added by Matthew/Spooky: Initialize variable to prevent errors.
    email = None

    if request.method == 'POST':
        # Added by Matthew/Spooky: Capture POST data for login.
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Added by Matthew/Spooky: Log user in.
            login(request, user)
            
            print(f"User {email} logged in.")
            print(f"Has Student Profile: {hasattr(user, 'students_student_profile')}")
            
            if Teacher.objects.filter(user=user).exists():
                return redirect("teacher_home")

            elif Student.objects.filter(user=user).exists():
                return redirect("student_home")
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
            print(f"Authentication failed for {email}")

    # Added by Matthew/Spooky: Render the signin page for GET request.
    return render(request, 'SignInPage.html')