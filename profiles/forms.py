from django import forms
from .models import Profile
# create your forms here


class ProfileEditForm(forms.ModelForm):
    full_name = forms.CharField(required=True)
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'email', 'national_code', 'image']