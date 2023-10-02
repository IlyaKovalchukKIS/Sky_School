from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='school/course/', verbose_name='картинка', **NULLABLE)
    description = models.TextField(max_length=350, verbose_name='описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(max_length=350, verbose_name='описание')
    preview = models.ImageField(upload_to='school/course/', verbose_name='картинка', **NULLABLE)
    url_video = models.URLField(verbose_name='ссылка', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'