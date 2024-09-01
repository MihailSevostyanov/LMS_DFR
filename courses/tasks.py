from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from courses.services import get_email_list



@shared_task
def send_information_about_course_update(pk):
    """Отправляет сообщение пользователю об обновлении курса"""

    message, email_list = get_email_list(pk)

    if email_list:
        print(email_list)
        send_mail(
            f"Обновление курса.",
            message,
            EMAIL_HOST_USER,
            email_list
        )
    else:
        print("no emails sended today")