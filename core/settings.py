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

# Added by Matthew/Spooky: These are layers that process requests and responses.
MIDDLEWARE = [

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Added by Matthew/Spooky: This tells django which file contains the main URL routing configuration.
ROOT_URLCONF = 'core.urls'

# Added by Matthew/Spooky: This section configures how django finds and loads HTML templates.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,

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
        'HOST': MONGO_URL,
    }
}

# Added by Matthew/Spooky: Authentication backend used for login.
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

# Added by Matthew/Spooky: STORAGES defines storage backends used by django.
STORAGES = {

    "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Added by Matthew/Spooky: Django password validation rules.
AUTH_PASSWORD_VALIDATORS = [

    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Added by Matthew/Spooky: Default language used by django.
LANGUAGE_CODE = 'en-us'

# Added by Matthew/Spooky: Timezone.
TIME_ZONE = 'CST'

# Added by Matthew/Spooky: Enables timezone-aware datetimes.
USE_TZ = True

# Added by Matthew/Spooky: URL prefix used to access static files.
STATIC_URL = '/static/'

# Added by Matthew/Spooky: Directory where collected static files are stored.
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')


# Added by Matthew/Spooky: STATICFILES_DIRS lists everywhere where django will search for static files like CSS, JS, and images.
STATICFILES_DIRS = [

    os.path.join(BASE_DIR, 'users/SignInPage/static'),
    os.path.join(BASE_DIR, 'users/MainHome/static'),
    os.path.join(BASE_DIR, 'users/TeacherRegistration/static'),
    os.path.join(BASE_DIR, 'users/StudentRegistration/static'),

    os.path.join(BASE_DIR, 'students/BaseStudent/static'),
    os.path.join(BASE_DIR, 'students/features/Calendar/static'),
    os.path.join(BASE_DIR, 'students/features/StudentHomePage/static'),
    os.path.join(BASE_DIR, 'students/features/Mentors/static'),
    os.path.join(BASE_DIR, 'students/features/Setting/static'),
    os.path.join(BASE_DIR, 'students/features/Progress/static'),
    os.path.join(BASE_DIR, 'students/features/Courses/static'),

    os.path.join(BASE_DIR, 'teachers/BaseTeacher/static'),
    os.path.join(BASE_DIR, 'teachers/features/Calendar/static'),
    os.path.join(BASE_DIR, 'teachers/features/teacher-courses/static'),
    os.path.join(BASE_DIR, 'teachers/features/TeacherHomePage/static'),
    os.path.join(BASE_DIR, 'teachers/features/tasks/static'),
    os.path.join(BASE_DIR, 'teachers/features/My_Student/static'),
    os.path.join(BASE_DIR, 'teachers/features/Setting/static'),
]