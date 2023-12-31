from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail

from main.models import Files
from config.settings import EMAIL_HOST_USER
from main.serializers import (
    DocumentSerializer,
    DocumentListSerializer,
    DocumentCheckSerializer,
    DocumentIdSerializer,
    DocumentAllSerializer,
)
from users.models import User


class DocumentCreateAPIView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        admin_users = User.objects.filter(is_staff=True)
        admin_email = admin_users.first().email

        # Отправка письма администратору с оповещением
        send_mail(
            subject="Новый документ",
            message=f"Вам пришел новый документ от {self.request.user.email}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[admin_email],
        )


class DocumentAPIView(generics.ListAPIView):
    serializer_class = DocumentListSerializer
    queryset = Files.objects.all()
    permission_classes = [IsAuthenticated]


class DocumentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = DocumentAllSerializer
    queryset = Files.objects.all()
    permission_classes = [IsAuthenticated]


class DocumentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = DocumentCheckSerializer
    queryset = Files.objects.all()
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        instance = serializer.instance

        # Выполняем обновление
        serializer.save()

        # Получаем значения после обновления
        status_after = serializer.instance.status

        if status_after != 3:
            # Проверяем изменения и выполняем нужные действия
            if status_after == 1:
                # Отправляем уведомление о принятии
                print("Документ принят")
                send_mail(
                    subject="Ответ администратора",
                    message=f"Ваш документ принят {self.request.user.email}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[instance.user.email],
                )

            if status_after == 2:
                # Отправляем уведомление об отклонении
                print("Документ отклонён")
                send_mail(
                    subject="Ответ администратора",
                    message=f"Ваш документ отклонён, попробуйте отправить его еще раз {self.request.user.email}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[instance.user.email],
                )


class DocumentDestroyAPIView(generics.DestroyAPIView):
    serializer_class = DocumentIdSerializer
    queryset = Files.objects.all()
    permission_classes = [IsAdminUser]
