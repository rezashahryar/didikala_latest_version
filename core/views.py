from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from .forms import LoginFormViaEmailOrMobile, RegisterViaEmailForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from .models import Activation
from .utils import send_activation_email
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib import messages

# Create your views here.


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LoginView(View):
    def get(self, request):
        return render(request, 'core/login.html')

    def post(self, request):
        login_form = LoginFormViaEmailOrMobile(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('pages:home_page_view')
            else:
                login_form.add_error("username", _("کاربری با این مشخصات ثبت نشده است"))
        else:
            login_form.add_error("username", _("لطفا اطلاعات کاربری خود را به درستی وارد کنید"))

        return render(request, 'core/login.html', {'login_form': login_form})


class RegisterView(GuestOnlyView, generic.CreateView):
    template_name = 'core/register.html'
    form_class = RegisterViaEmailForm

    def form_valid(self, form):
        user = form.save(commit=False)
        cd = form.cleaned_data

        if settings.DISABLE_USERNAME:
            user.first_name = f'user_{user.id}'

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        # Create a user record
        user.email = cd['email']
        user.set_password(cd['password'])
        user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.save()
            send_activation_email(self.request, user.email, code)

            messages.success(
                self.request, _('حساب کاربری شما ساخته شد.جهت فعالسازی وارد لینک ارسال شده به ایمیل خود شوید.'))
        else:
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=raw_password)
            login(self.request, user)

            messages.success(self.request, _('شما با موفقیت ثبتنام کردید'))

        return redirect('pages:home_page_view')


class ActivateView(View):

    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Activate profile
        user = act.user
        user.is_active = True
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('فعالسازی اکانت شما با موفقیت انجام شد'))

        return redirect('core:login_view')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('pages:home_page_view')
