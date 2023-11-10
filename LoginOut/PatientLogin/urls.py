from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('PatientLogin/',views.PatientLogin,name='PatientLogin'),
    path('PatientSignup/',views.PatientSignup,name='PatientSignup'),
]
