from django import forms 

from apps.account.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'website', 'bio', 'phone', 'city', 'country',)

