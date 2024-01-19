from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Order
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
# Create your views here.


@login_required()
def profile_view(request):
    profile = request.user.profile
    if not profile:
        return redirect('profiles:profile_main_page')
    orders = request.user.orders.all()[:3]
    context = {
        "profile": profile,
        "orders": orders
    }
    return render(request, 'profiles/profile.html', context)


@login_required()
def profile_order_list_view(request):
    return render(request, 'profiles/order_list.html')


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