from django.http import HttpResponse
import requests
import json
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views import View, generic
from django.http import HttpResponse
from django.contrib import messages
import shop.forms
from .cart import Cart
from products.models import Product
from .forms import CouponApplyForm, OrderForm, AddressForm, InfoOrderForm
from .models import Coupon, Order, OrderItem, Address
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
# Create your views here.

FORMS = [("info_order_form", shop.forms.InfoOrderForm)]

TEMPLATES = {"info_order_form": "shop/shop.html"}


def pay_by_credit_card(wizard):
    """Return true if user opts to pay by credit card"""
    # Get cleaned data from payment step
    cleaned_data = wizard.get_cleaned_data_for_step('info_order_form')
    print(cleaned_data)
    # Return true if the user selected credit card
    return cleaned_data


# class ContactWizard(SessionWizardView):
#     # form_list = [OrderForm, AddressForm]
#     condition_dict = {"info_order_form": pay_by_credit_card}
#     def get_template_names(self):
#         return TEMPLATES[self.steps.current]
#
#     def done(self, form_list, **kwargs):
#         print("*" * 40)
#         print(form.cleaned_data for form in form_list)
#         print("*" * 40)
#         return HttpResponseRedirect('pages:home_page_view')
#         # return render(self.request, 'shop/test.html', {
#         #     'form_data': [form.cleaned_data for form in form_list],
#         # })

class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        if cart:
            return render(request, 'shop/cart_detail.html', {'cart': cart, "coupon_form": CouponApplyForm()})
        else:
            return render(request, 'shop/cart_empty.html')


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.sales_number += 1
        product.save()
        color, quantity = request.POST.get('color'), request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product, quantity, color)
        return redirect('shop:cart_detail')


class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('shop:cart_detail')


class CartDeleteViewFromHomePage(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('pages:home_page_view')


@require_POST
def coupon_apply_view(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('shop:payment_page')


@login_required()
def information_order(request):
    address_form = AddressForm()
    order_form = OrderForm()
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, _('سبد خرید شما خالی است'))
        return redirect('pages:home_page_view')
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            new_order = order_form.save(commit=False)
            new_order.user = request.user
            new_order.save()

            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=new_order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price,
                )
                product.sales_number += 1
                product.save()
            cart.clear()
            messages.success(request, _('سفارش شما با موفیقت ثبت شد'))
            return redirect('pages:home_page_view')

    context = {
        'address_form': address_form,
        'order_form': order_form,
        'info_order': InfoOrderForm(),
    }
    return render(request, 'shop/shop.html', context)


def add_new_address(request):
    address_form = AddressForm()
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect('shop:information_order_view')
    return render(request, 'shop/add_new_address.html', {'address_form': address_form})


class EditAddressView(generic.UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'shop/edit_address.html'
    success_url = reverse_lazy('shop:information_order_view')


def payment_page(request):
    return render(request, 'shop/payment_page.html')


@require_GET
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    address.delete()
    return redirect('shop:information_order_view')


def payment_process(request):
    return render(request, 'shop/payment_process.html')


def payment_proccess(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        'accept': 'application/json',
        'content_type': 'application/json',
    }

    request_data = {
        'merchant_id': '36 char',
        'amount': rial_total_price,
        'description': f'#{order.id}: {order.user.first_name}',
        'callback_url': 'http://127.0.0.1:8000' + reverse('payment:payment_callback'),
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
    else:
        return HttpResponse('error from zarinpal')


def payment_call_back_view(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content_type': 'application/json',
        }

        request_data = {
            'merchant_id': '36 char',
            'amount': rial_total_price,
            'authority': payment_authority,
        }

        res = requests.post(
            url='https://api.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header
        )

        if 'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.zarinpal_ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse(_('پرداخت شما با موفقیت انجام شد'))
            elif payment_code == 101:
                return HttpResponse(_("این تراکنش قبلا ثبت شده است"))
            else:
                return HttpResponse(_('تراکنش ناموفق بود'))

    else:
        return HttpResponse(_('تراکنش ناموفق بود'))


# def payment_process_sandbox(request):
#     order_id = request.session.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#
#     toman_total_price = order.get_total_price()
#     rial_total_price = toman_total_price * 10
#
#     zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
#
#     request_header = {
#         'accept': 'application/json',
#         'content_type': 'application/json',
#     }
#
#     request_data = {
#         'MerchantID': 'abcabcabcabcabcabcabcabcabcabcabcabc',
#         'Amount': rial_total_price,
#         'Description': f'#{order.id}: {order.user.first_name}',
#         'CallbackURL': 'http://127.0.0.1:8000' + reverse('payment:payment_callback'),
#     }
#
#     res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
#
#     data = res.json()
#     authority = data['Authority']
#     order.zarinpal_authority = authority
#     order.save()
#
#     if 'errors' not in data or len(data['errors']) == 0:
#         return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}')
#     else:
#         return HttpResponse('error from zarinpal')


# def payment_call_back_sandbox_view(request):
#     payment_authority = request.GET.get('Authority')
#     payment_status = request.GET.get('status')
#
#     order = get_object_or_404(Order, zarinpal_authority=payment_authority)
#     toman_total_price = order.get_total_price()
#     rial_total_price = toman_total_price * 10
#
#     if payment_status == 'OK':
#         request_header = {
#             'accept': 'application/json',
#             'content_type': 'application/json',
#         }
#
#         request_data = {
#             'MerchantID': 'abcabcabcabcabcabcabcabcabcabcabcabc',
#             'Amount': rial_total_price,
#             'Authority': payment_authority,
#         }
#
#         res = requests.post(
#             url='https://api.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
#             data=json.dumps(request_data),
#             headers=request_header
#         )
#
#         if 'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
#             data = res.json()
#             payment_code = data['Status']
#
#             if payment_code == 100:
#                 order.is_paid = True
#                 order.zarinpal_ref_id = data['RefID']
#                 order.zarinpal_data = data
#                 order.save()
#
#                 return HttpResponse('پرداخت شما با موفقیت انجام شد')
#             elif payment_code == 101:
#                 return HttpResponse("این تراکنش قبلا ثبت شده است")
#             else:
#                 return HttpResponse('تراکنش ناموفق بود')
#
#     else:
#         return HttpResponse('تراکنش ناموفق بود')