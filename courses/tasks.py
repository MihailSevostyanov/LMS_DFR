from datetime import datetime, timedelta, timezone

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from courses.models import Course
from courses.services import get_email_list
from users.models import Subscriptions


@shared_task
def send_information_about_course_update(pk):
    """Отправляет сообщение пользователю об обновлении курса"""
    subscriptions = Subscriptions.objects.filter(course=pk)
    course = Course.objects.get(pk=pk)

    message = f"Ваш курс {course.title} был обновлен!"
    email_list = subscriptions.values_list("user_email", flat=True)

    if email_list:
        print(email_list)
        send_mail(f"Обновление курса.", message, EMAIL_HOST_USER, email_list)
