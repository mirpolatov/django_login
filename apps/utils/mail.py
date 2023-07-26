from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.utils.token import one_time_token
from root.settings import EMAIL_HOST_USER


def send_to_gmail(user, domain, _type='activation'):
    print('ACCEPT TASK')

    context = {
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(str(user.pk))),
        'token': one_time_token.make_token(user),
    }
    subject = 'Activate your account'
    template = 'activation.html'
    if _type == 'reset':
        subject = 'Trouble signing in?'
        template = 'reset_password.html'
    elif _type == 'change':
        subject = ''

    message = render_to_string(f'email_templates/{template}', context)

    recipient_list = [user.email]

    email = EmailMessage(subject, message, EMAIL_HOST_USER, recipient_list)
    email.content_subtype = 'html'
    result = email.send()
    print('Send to MAIL', template)
    return result
