from django.db import models
from django.conf import settings

FILE_STATUS = [(1, 'Принято'), (2, 'Отклонено'), (3, 'На проверке')]


class Files(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Пользователь')

    file = models.FileField(upload_to='files/', verbose_name='Файл')
    status = models.PositiveSmallIntegerField(choices=FILE_STATUS, default=3)

    def __str__(self):
        return f'Файл {self.user}: Статус {self.status}'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
