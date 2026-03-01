# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, Feedback, home_view
# Uses custom Login class
from .views import CustomLoginView

urlpatterns = [
    path(
        'login/',
        CustomLoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    #Added by Matthew/Spooky to define route.
    path('Feedback/', Feedback, name='Feedback'),
]