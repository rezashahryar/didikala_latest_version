from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from shop.models import Order, Address, OrderItem
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ProfileEditForm
from shop.forms import AddressForm
from django.db.models import Prefetch
# Create your views here.


@login_required()
def profile_view(request):
    profile = request.user.profile
    if not profile:
        return redirect('profiles:profile_main_page')
    orders = Order.objects.prefetch_related('items').filter(user=request.user)[:3]
    context = {
        "profile": profile,
        "orders": orders
    }
    return render(request, 'profiles/profile.html', context)


def add_new_address(request):
    address_form = AddressForm()
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect('profiles:add_address_view')
    return render(request, 'profiles/user_addresses.html', {'address_form': address_form})


class EditAddressView(generic.UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'shop/edit_address.html'
    success_url = reverse_lazy('profiles:add_address_view')


@require_POST
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk)
    address.delete()
    return redirect('profiles:user_addresses')


@login_required()
def profile_order_list_view(request):
    orders = Order.objects.prefetch_related('items').filter(user=request.user)
    return render(request, 'profiles/order_list.html', {'order_list': orders})


@login_required()
def profile_additional_info_view(request):
    return render(request, 'profiles/profile_additional_info.html')


@login_required()
def profile_additional_info_change_view(request):
    return render(request, 'profiles/profile_additional_info_change.html')


@login_required()
def order_detail(request, pk):
    order = get_object_or_404(Order, id=pk)
    return render(request, 'profiles/order_detail.html', {"order": order})


@login_required()
def profile_user_orders_return(request):
    return render(request, 'profiles/user_orders_return.html')


@login_required()
def profile_edit_view(request):
    if request.method == 'POST':
        profile_edit_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_edit_form.is_valid():
            profile_edit_form.save()
            return redirect('profiles:profile_main_page')
    else:
        profile_edit_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'profile_edit_form': profile_edit_form,
    }
    return render(request, 'profiles/profile_edit.html', context)


def user_comments(request):
    return render(request, 'profiles/user_comments.html')


def user_addresses(request):
    return render(request, 'profiles/user_addresses.html')