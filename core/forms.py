from django import forms
from core.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class LoginFormViaEmailOrMobile(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     if len(username) < 6:
    #         raise forms.ValidationError('اسم اشتباه')


class RegisterViaEmailForm(forms.ModelForm):
    password = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['mobile']

    # def clean(self):
    #     cleaned_data = super(RegisterViaEmailForm, self).clean()
    #     email = self.cleaned_data.get('email')
    #     mobile = self.cleaned_data.get('mobile')
    #
    #     user = User.objects.get(mobile=mobile)
    #
    #     if user is not None:
    #         raise forms.ValidationError('این شماره موبایل قبلا ثبت شده است')
    #     elif User.objects.get(email=email):
    #         raise forms.ValidationError('این ایمیل قبلا ثبت شده است')
    #     return cleaned_data
