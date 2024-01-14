from django import forms
from core.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q


class UserCacheMixin:
    user_cache = None


class LoginFormViaEmailOrMobile(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    remember_me = forms.BooleanField(required=False)

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
    #     try:
    #         user = User.objects.filter(Q(email=email) | Q(mobile=mobile))
    #         if user:
    #             raise ValidationError(_('کاربری با این مشخصات از قبل ثبتانم کرده است'))
    #     except:
    #         return cleaned_data
    #
    #     return cleaned_data


class EmailOrUsernameForm(forms.Form):
    email_or_username = forms.CharField(label=_('Email or Username'))

    # def clean_email_or_username(self):
    #     email_or_username = self.cleaned_data['email_or_username']
    #
    #     user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
    #     if not user:
    #         raise ValidationError(_('You entered an invalid email address or username.'))
    #
    #     if not user.is_active:
    #         raise ValidationError(_('This account is not active.'))
    #
    #     self.user_cache = user
    #
    #     return email_or_username


class EmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_('Email'))

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #
    #     user = User.objects.filter(email__iexact=email).first()
    #     if not user:
    #         raise ValidationError(_('You entered an invalid email address.'))
    #
    #     if not user.is_active:
    #         raise ValidationError(_('This account is not active.'))
    #
    #     self.user_cache = user
    #
    #     return email


class RestorePasswordViaEmailOrUsernameForm(UserCacheMixin, EmailOrUsernameForm):
    pass


class RestorePasswordForm(EmailForm):
    pass
