from django import forms
from .models import Order, Address
from django.utils.translation import gettext_lazy as _
from core.models import User
from django.contrib.auth import get_user_model


class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=50, label=_('کد تخفیف'))


class InfoOrderForm(forms.Form):
    address = forms.ModelChoiceField(label=_('آدرس'), queryset=Address.objects.all())


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'order_notes', 'post_code']
        widgets = {
            'order_notes': forms.Textarea(attrs={'rows': 5}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('full_name', 'mobile_number', 'province', 'city', 'address', 'post_code')

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if not mobile_number.isdigit():
            raise forms.ValidationError("این شماره موبایل صحیح نیست")
        return mobile_number

    def clean_post_code(self):
        post_code = self.cleaned_data['post_code']
        if not post_code.isdigit():
            raise forms.ValidationError("کد پستی فقط شامل اعداد می شود")
        elif len(post_code) > 10:
            raise forms.ValidationError("کد پستی شامل 10 عدد می شود")
        elif len(post_code) < 10:
            raise forms.ValidationError("کد پستی شامل 10 عدد می شود")
        return post_code
