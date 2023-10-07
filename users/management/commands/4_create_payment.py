import random

from django.core.management import BaseCommand
from django.utils import timezone

from school.models import Payment, Course, Lesson
from users.models import User

PAYMENTS = [
    {
        'user': User.objects.get(pk=2),
        'course_payment': Course.objects.get(pk=random.randint(1, 3)),
        'date_payment': str(timezone.now()),
        'payment_amount': random.randint(100_000, 249_000),
        'payment_method': random.choice(['card', 'cash'])
    },
    {
        'user': User.objects.get(pk=3),
        'course_payment': Course.objects.get(pk=random.randint(1, 3)),
        'date_payment': str(timezone.now()),
        'payment_amount': random.randint(100_000, 249_000),
        'payment_method': random.choice(['card', 'cash'])
    },
    {
        'user': User.objects.get(pk=4),
        'lesson_payment': Lesson.objects.get(pk=random.randint(1, 3)),
        'date_payment': str(timezone.now()),
        'payment_amount': random.randint(100_000, 249_000),
        'payment_method': random.choice(['card', 'cash'])
    },
    {
        'user': User.objects.get(pk=5),
        'lesson_payment': Lesson.objects.get(pk=random.randint(1, 3)),
        'date_payment': str(timezone.now()),
        'payment_amount': random.randint(100_000, 249_000),
        'payment_method': random.choice(['card', 'cash'])
    },

]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for payment in PAYMENTS:
            payment_create = Payment.objects.create(
                user=payment['user'],
                course_payment=payment.get('course_payment') if payment.get('course_payment') else None,
                lesson_payment=payment.get('lesson_payment') if payment.get('lesson_payment') else None,

                date_payment=payment['date_payment'],
                payment_amount=payment['payment_amount'],
                payment_method=payment['payment_method']
            )

            payment_create.save()
