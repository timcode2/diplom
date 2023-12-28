from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_approval_notification(user_email):
    send_mail(
        subject="Ответ администратора",
        message=f"Ваш документ принят {user_email}",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
    )


def send_rejection_notification(user_email):
    send_mail(
        subject="Ответ администратора",
        message=f"Ваш документ отклонён, попробуйте отправить его еще раз {user_email}",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
    )
