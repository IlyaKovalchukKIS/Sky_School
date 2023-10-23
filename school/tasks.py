from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from school.models import Subscription
from users.models import User


@shared_task
def check_update(pk_course: int):
    course = Subscription.objects.filter(course=pk_course, is_active=True)
    recipient = [recipient.student.email for recipient in course]

    print(recipient)

    send_mail(
        "Обновление курса",
        "Курс обновился, ура!",
        settings.EMAIL_HOST_USER,
        recipient_list=recipient,
        fail_silently=False,
    )


@shared_task
def is_active_user():
    users = User.objects.all()
    time_now = timezone.now()
    for user in users:
        user_last_login = time_now - user.last_login
        print(user_last_login)
        if user_last_login.day > 30:
            user.is_active = False
