from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    amount = models.IntegerField(verbose_name='стоимость', default=1000)
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='school/course/', verbose_name='картинка', **NULLABLE)
    description = models.TextField(max_length=350, verbose_name='описание')
    url_video = models.URLField(verbose_name='ссылка', **NULLABLE)
    date_update = models.DateTimeField(verbose_name='время обновления', auto_now=timezone.now())

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    amount = models.IntegerField(verbose_name='стоимость', default=1000)
    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.CASCADE, **NULLABLE)
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(max_length=350, verbose_name='описание')
    preview = models.ImageField(upload_to='school/course/', verbose_name='картинка', **NULLABLE)
    url_video = models.URLField(verbose_name='ссылка', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    PAYMENT_METHOD = [
        ('card', 'карта'),
        ('cash', 'наличные')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    course_payment = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс',  **NULLABLE)
    lesson_payment = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок',  **NULLABLE)

    date_payment = models.DateTimeField(verbose_name='дата платежа', **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} {self.course_payment if self.course_payment else self.lesson_payment}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
        ordering = ('-date_payment',)


class Subscription(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    is_active = models.BooleanField(verbose_name='активно', default=False)

    def __str__(self):
        return f'{self.student} {self.course}'

    class Meta:
        verbose_name = 'подписка на обновления'
        verbose_name_plural = 'подписки на обновления'