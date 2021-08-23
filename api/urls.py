#from knox import views as knox_views
from .views import RegisterAPI, ChangePasswordView
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
   
]