from django import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms import widgets

from .models import (

    # CustomUser
    CustomUser,

    # Company
    Company,

    # User profile imports. 
    Reference,
    Language,
    WorkExperience,
    Training,
    Education,
    UserProfile,
    Company,
    CustomUser

)


class JobSeekerLoginForm(forms.Form):
    email = forms.EmailField(max_length=100, error_messages={'required': 'Please enter your registered email'})
    password = forms.CharField(max_length=100, error_messages={'required': 'Please enter your valid password'})


class JobSeekerLoginForm(forms.Form):
    email = forms.EmailField(help_text="Your email address", error_messages={'required': "Please enter a valid email"})
    password = forms.CharField(
        help_text="Your password",
        max_length=255,
        widget=forms.PasswordInput,
        error_messages={'required': "Please enter a valid password"})


class JobSeekerRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(max_length=255, error_messages={'required': 'Fullname is required'})
    mobile = forms.CharField(widget=forms.NumberInput(), max_length=10,
                             error_messages={'required': 'Mobile no is required'})
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'mobile', 'password', 'confirm',)

    def clean_confirm(self):
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']

        if password != confirm or len(password) <= 0:
            raise forms.ValidationError("Password mismatch")

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not mobile.isdigit() or len(mobile) > 10:
            raise forms.ValidationError("Mobile number should contain at most 10 characters ")


class EmployerLoginForm(JobSeekerLoginForm):
    pass


class EmployerRegistrationForm(forms.ModelForm):
    organization_name = forms.CharField(max_length=255, error_messages={'required': 'Organization name is required'})
    confirm_password = forms.CharField(widget=forms.PasswordInput, error_messages={'required': 'Password is required',
                                                                                   'invalid': 'Use 8 or more characters with a mix of letters, numbers & symbols'})

    class Meta:
        model = CustomUser
        fields = ('organization_name', 'email', 'password', 'confirm_password')
        widgets = {
            'password': widgets.PasswordInput
        }

    def clean_confirm_password(self):
        import re
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError("Password is mismatched")

        if len(password) < 8:
            raise forms.ValidationError("Password length should be at least 8 characters")

        elif not re.match('[A-Za-z0-9]', password):
            raise forms.ValidationError("Password must contain Uppercase, Lowercase, Number and Special symbols")


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        exclude = ('user', 'is_active', 'is_deleted',)


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        exclude = ('user', 'is_active', 'is_deleted', 'listening', 'learning')


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ('is_active', 'is_deleted', 'currently_working_here', 'user')


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        exclude = ('is_active', 'is_deleted', 'user')


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['user', 'is_active', 'is_deleted', 'current_studying_here']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


# CustomUser
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


# Company Forms
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
