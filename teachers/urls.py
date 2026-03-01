from django.urls import path
from . import views

urlpatterns = [

    path('Feedback/', views.Feedback, name='Feedback'),
]