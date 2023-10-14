from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from school.models import Lesson
from users.models import User


class SchoolTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='test')
        self.client.force_authenticate(user=self.user)
        self.user.is_superuser = True
        self.user.is_staff = True

    def test_create_lesson(self):
        """ Тестирование создания урока """
        data = {
            'name': 'Test 1',
            'description': 'Create lesson',
            'url_video': 'https://www.youtube.com/'
        }
        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': 1, 'name': 'Test 1', 'description': 'Create lesson', 'preview': None,
             'url_video': 'https://www.youtube.com/', 'owner': 1, 'course': None}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        user_test = User.objects.create(email='test@test.ru', password='123qwe456rty')
        Lesson.objects.create(owner=user_test, name='Test 2', description='test_list_lesson')

        response = self.client.get(
            '/lesson/list/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            ({'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': 1, 'name': 'Test 2', 'description': 'test_list_lesson', 'preview': None, 'url_video': None,
                 'owner': 2, 'course': None}]})
        )
