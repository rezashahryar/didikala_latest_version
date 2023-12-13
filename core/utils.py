from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



def send_mail(to, template, context):
    html_content = render_to_string(f'core/emails/{template}.html', context)
    text_content = render_to_string(f'core/emails/{template}.txt', context)

    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_activation_email(request, email, code):
    context = {
        'subject': _('user activation'),
        'uri': request.build_absolute_uri(reverse('core:activate_user', kwargs={'code': code})),
    }

    send_mail(email, 'activate_user', context)