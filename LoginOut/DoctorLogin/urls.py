from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('DoctorLogin/',views.login,name='DoctorLogin'),
    path('DoctorSignup/',views.signup,name='DoctorSignup'),
]
