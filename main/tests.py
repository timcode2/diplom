from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from main.models import Files
from users.models import User


class DocumentTest(TestCase):
    def setUp(self):
        # Добавляем Юзера
        self.user = User.objects.create(
            email='test@sky.pro',
            password='userpassword',
        )
        self.user.save()
        # Добавляем администратора
        self.admin_user = User.objects.create(
            email='admin@sky.pro',
            password='adminpassword',
            is_staff=True,
        )
        self.admin_user.save()
        self.client = APIClient()

    def test_document_creation(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

        # Формируем тестовый файл
        file_content = b"file_content"
        test_file = SimpleUploadedFile("test.ods", file_content)

        # Данные для POST-запроса
        data = {'file': test_file}

        # Выполнение POST-запроса
        response = self.client.post(reverse('main:create'), data, format='multipart')
        # Проверка корректного ответа и создания объекта
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Files.objects.count(), 1)

        # Проверка отправки письма
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Новый документ')
        self.assertEqual(mail.outbox[0].to, [self.admin_user.email])

        # Проверка, что атрибут user объекта совпадает с текущим пользователем
        self.assertEqual(Files.objects.first().user, self.user)