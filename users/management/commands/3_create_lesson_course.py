from django.core.management import BaseCommand

from school.models import Course, Lesson

COURSES = [
    ['Python-develop', 'Python course develop'],
    ['Java-develop', 'Java course develop'],
    ['Web-develop', 'Web course develop'],
]

LESSONS = [
    ['Django', 'Django lesson', 1],
    ['Django Rest Framework', 'Django Rest Framework lesson', 1],
    ['OOP', 'OOP lesson', 1],
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for course in COURSES:
            course_create = Course.objects.create(
                name=course[0],
                description=course[1],
            )

            course_create.save()

        for lesson in LESSONS:
            lesson_create = Lesson.objects.create(
                course=Course.objects.get(pk=lesson[2]),
                name=lesson[0],
                description=lesson[1],
            )

            lesson_create.save()
