from django import forms
from .models import Order


class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=50, label='کد تخفیف')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'order_notes']
        widgets = {
            'order_notes': forms.Textarea(attrs={'rows': 5})
        }