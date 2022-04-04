from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from .views import (
    jobseeker_login,
    jobseeker_registration,
    employer_login,
    employer_registration,
    email_verification,
    PasswordChangeView

)

app_name = 'account'

urlpatterns = [

    # Jobseeker auth 
    path('jobseeker/login', jobseeker_login, name="jobseeker-login"),
    path('jobseeker/registration', jobseeker_registration, name='jobseeker-registration'),

    # Employer auth
    path('employer/login', employer_login, name='employer-login'),
    path('employer/registration', employer_registration, name='employer-registration'),

    # Email Verification
    path('email-verification/<str:email>', email_verification, name='registered-email-verification'),

    # Logout all user.
    path('logout/', LogoutView.as_view(), name="logout"),

    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
