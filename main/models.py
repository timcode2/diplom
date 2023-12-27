from django.db import models
from django.conf import settings


class Files(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Пользователь')

    file = models.FileField(upload_to='files/', verbose_name='Файл')
    accept_file = models.BooleanField(default=False, verbose_name='Принятый файл')
    denied_file = models.BooleanField(default=False, verbose_name='Отклонённый файл')

    def __str__(self):
        return f'Файл {self.user}: Принят - {self.accept_file} Отклонён - {self.denied_file}'

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
