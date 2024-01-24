from django import forms
from .models import Profile
# create your forms here


class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number', 'email', 'national_code', 'image']
        required = ['full_name', 'phone_number', 'email', 'national_code', 'image']