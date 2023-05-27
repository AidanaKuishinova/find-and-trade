from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

def send_reset_password_mail(email, token, id):
    print('hello')
    subject = 'Сброс пароля'
    html_message = loader.render_to_string(
        'main/mail_body.html',
        {
            'username': email,
            'link': f'http://127.0.0.1:8000/reset/{id}/{token}'
        }
    )
    message = f'http://127.0.0.1:8000/reset/{id}/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list, html_message=html_message)


def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%', "*"]
    val = True

    if len(passwd) < 6:
        print('length should be at least 6')
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        val = False
    return val