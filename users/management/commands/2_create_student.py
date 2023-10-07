from django.core.management import BaseCommand

from users.models import User

STUDENTS = [
    ['Andrey@student.ru', 'Andrey', 'Pavlov', '123'],
    ['Alex@student.ru', 'Alex', 'Fedorov', '123'],
    ['Sergey@student.ru', 'Sergey', 'Frolov', '123'],
    ['Stas@student.ru', 'Stas', 'Dworezkij', '123']
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for student in STUDENTS:
            user = User.objects.create(
                email=student[0],
                first_name=student[1],
                last_name=student[2],
            )

            user.set_password(student[3])
            user.save()