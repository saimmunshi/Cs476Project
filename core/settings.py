import os
from pathlib import Path
from dotenv import load_dotenv

# Added by Matthew/Spooky: This stores the the root directory.
BASE_DIR = Path(__file__).resolve().parent.parent

# Added by Matthew/Spooky: Loading the .env file so its variables can be accessed using os.getenv().
load_dotenv()

# Added by Matthew/Spooky: Getting the mongodb URL from the .env file.
MONGO_URL = os.getenv("MONGO_URL")

# Added by Matthew/Spooky: This is used by django for security features.
SECRET_KEY = 'django-insecure-%+%!%)p1s=okt4lx6jqj^i18-@s+ul4@*2ni8vr@5+vg@m0*em'

# Added by Matthew/Spooky: Temp for testing.
DEBUG = True

# Added by Matthew/Spooky: Defines which domains django can use. For now just localhost.
ALLOWED_HOSTS = []

# Added by Matthew/Spooky: This tells django which apps are active.
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'teachers',
    'students',
    'courses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS tells Django to look for a root 'templates' folder for your Sidebar/Base
        'DIRS': [
            #Users App Connection Logic:
            os.path.join(BASE_DIR, 'users/MainHome/templates'),
            os.path.join(BASE_DIR, 'users/TeacherRegistration/templates'),
            os.path.join(BASE_DIR, 'users/StudentRegistration/templates'),
            os.path.join(BASE_DIR, 'users/SignInPage/templates'),

            # Student App templates (This is likely where BaseStudent.html lives)
            os.path.join(BASE_DIR, 'students/BaseStudent/templates'), 
            os.path.join(BASE_DIR, 'students/features'),

            # Teacher App templates
            os.path.join(BASE_DIR, 'teachers/BaseTeacher/templates'),
            os.path.join(BASE_DIR, 'teachers/features'),




            """
            BASE_DIR / 'users' / 'TeacherRegistration' / 'templates',
            BASE_DIR / 'users' / 'StudentRegistration' / 'templates',
            BASE_DIR / 'users' / 'SignInPage' / 'templates',
            BASE_DIR / 'users' / 'MainHome' / 'templates',

            #Student App Connection Logic
            BASE_DIR / 'students' / 'BaseStudent'/ 'templates',
            BASE_DIR / 'students' / 'features' / 'Courses' / 'templates',
            BASE_DIR / 'students' / 'features' / 'StudentHomePage' / 'templates',

            #Teacher App Connection Logic
            BASE_DIR / 'teachers' / 'BaseTeacher'/ 'templates',
            BASE_DIR / 'teachers' / 'features' / 'TeacherHomePage' / 'templates',
            BASE_DIR / 'teachers' / 'features' / 'Create_Task' / 'templates',
            """
            ], 
        'APP_DIRS': True, # This allows Django to find students/features/Calender/templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Added by Matthew/Spooky: This defines the callable used by web servers to interact with django.
WSGI_APPLICATION = 'core.wsgi.application'

# Added by Matthew/Spooky: This defines the custom user model used.
AUTH_USER_MODEL = 'users.CustomUser'

# Added by Matthew/Spooky: Database configuration using mongodb.
DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_backend',
        'NAME': 'MentoringAppDB',
        'HOST': os.getenv('MONGO_URL'),
        # DO NOT put DEFAULT_AUTO_FIELD here!
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Added by Matthew/Spooky: This sets the default primary key field type for models.
DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'

# Added by Matthew/Spooky: Silences specific mongodb system warnings from django.
SILENCED_SYSTEM_CHECKS = ['mongodb.E001']

# Added by Matthew/Spooky: Cloudinary configuration used to store uploaded profile pictures or documents.
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.getenv('CLOUDINARY_URL')
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
#Added By Sam MongoDb does not auto incrment numbers so the buttom code is to help
DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'
SILENCED_SYSTEM_CHECKS = ['mongodb.E001']

"""
#Orginal code for Sqllite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Where to go after a successful manual login if no 'next' parameter is present
###LOGIN_REDIRECT_URL = 'teacher_home' 

# Where the login page lives
##LOGIN_URL = 'signin_page_view'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
#Added By Saim Munshi: combines based folder to path to the feature directories 
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

STATICFILES_DIRS =[

    ###### Users App Connection#########
    #Added By Saim Munshi: This is to connect the main base folder to the user Login Page Application features in static directory.  
    
    os.path.join(BASE_DIR, 'users/SignInPage/static'),
    #Added By Saim Munshi: This is to connect the main base folder to the user Main Page Application features in static directory.  

    os.path.join(BASE_DIR, 'users/MainHome/static'),


    #Added By Saim Munshi: This is to connect the main base folder to the user Registration Application features in static directory.  
     os.path.join(BASE_DIR, 'users/TeacherRegistration/static'),
     os.path.join(BASE_DIR, 'users/StudentRegistration/static'),
    ###### Student App Connection#########
    #Added By Saim Munshi: This is to connect the main base folder to the Student Application features in static directory.  
    os.path.join(BASE_DIR, 'students/BaseStudent/static'),
    os.path.join(BASE_DIR, 'students/features/Calendar/static'), # Updated spelling
    os.path.join(BASE_DIR, 'students/features/StudentHomePage/static'),
    os.path.join(BASE_DIR, 'students/features/Mentors/static'),
    os.path.join(BASE_DIR, 'students/features/Setting/static'),
    os.path.join(BASE_DIR, 'students/features/Progress/static'),
    os.path.join(BASE_DIR, 'students/features/Courses/static'),

    ###### Teacher App Connection#########
    #Added By Saim Munshi: This is to connect the main base folder to the Teacher Application features in static directory. 
    os.path.join(BASE_DIR, 'teachers/BaseTeacher/static'),
    os.path.join(BASE_DIR, 'teachers/features/Calendar/static'), 
    os.path.join(BASE_DIR, 'teachers/features/teacher-courses/static'), 
    os.path.join(BASE_DIR, 'teachers/features/TeacherHomePage/static'),
    os.path.join(BASE_DIR, 'teachers/features/tasks/static'), 
    os.path.join(BASE_DIR, 'teachers/features/My_Student/static'), 
    os.path.join(BASE_DIR, 'teachers/features/Setting/static'),
    os.path.join(BASE_DIR, 'teachers/BaseTeacher/static'),

    #Added by: Matthew/Spooky.
    os.path.join(BASE_DIR, 'courses/static'),
]

from django.core.servers.basehttp import WSGIServer
