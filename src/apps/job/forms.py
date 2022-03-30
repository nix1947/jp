from django import forms

from apps.account.models import Reference

from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job 
        fields = (
            'title', 
            'description',
            'job_category', 
            'employment_type',
            'job_education',
            'no_of_vacancies',
            'skills',
            'experience',
            'job_level',
            'job_location',
            'job_industry',
            'offered_salary',
            'what_we_offer',
            'apply_method',
            'deadline',
            )


