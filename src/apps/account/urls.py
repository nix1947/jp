from django.urls import path

from .views import (
    LoginView,
    jobseeker_login,
    jobseeker_registration,
    employer_login,
    employer_registration,
    email_verification

)


app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),

    # Jobseeker auth 
    path('jobseeker/login', jobseeker_login, name="jobseeker-login"),
    path('jobseeker/registration', jobseeker_registration, name='jobseeker-registration'),

    # Employer auth
    path('employer/login', employer_login, name='employer-login'),
    path('employer/registration', employer_registration, name='employer-registration'),

    # Email Verification
    path('email-verification/<str:email>', email_verification, name='registered-email-verification')
    
   
]
   