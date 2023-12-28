from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail

from main.models import Files
from config.settings import EMAIL_HOST_USER
from main.serializers import DocumentSerializer, DocumentListSerializer, DocumentCheckSerializer, DocumentIdSerializer, \
    DocumentAllSerializer
from users.models import User


def send_approval_notification(user_email):
    send_mail(
        subject='Ответ администратора',
        message=f'Ваш документ принят {user_email}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email]
    )


def send_rejection_notification(user_email):
    send_mail(
        subject='Ответ администратора',
        message=f'Ваш документ отклонён, попробуйте отправить его еще раз {user_email}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email]
    )


class DocumentCreateAPIView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        admin_users = User.objects.filter(is_staff=True)
        admin_email = admin_users.first().email

        # Отправка письма администратору с оповещением
        send_mail(
            subject='Новый документ',
            message=f'Вам пришел новый документ от {self.request.user.email}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[admin_email]
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

        # Получаем значения до и после обновления
        accept_file_before = instance.accept_file
        denied_file_before = instance.denied_file

        # Выполняем обновление
        serializer.save()

        # Получаем значения после обновления
        accept_file_after = serializer.instance.accept_file
        denied_file_after = serializer.instance.denied_file

        if accept_file_after != denied_file_after:
            # Проверяем изменения и выполняем нужные действия
            if accept_file_before != accept_file_after and accept_file_after:
                # Отправляем уведомление о принятии
                print('Документ принят')
                send_mail(
                    subject='Ответ администратора',
                    message=f'Ваш документ принят {self.request.user.email}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[instance.user.email]
                )

            if denied_file_before != denied_file_after and denied_file_after:
                # Отправляем уведомление об отклонении
                print('Документ отклонён')
                send_mail(
                    subject='Ответ администратора',
                    message=f'Ваш документ отклонён, попробуйте отправить его еще раз {self.request.user.email}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[instance.user.email]
                )


class DocumentDestroyAPIView(generics.DestroyAPIView):
    serializer_class = DocumentIdSerializer
    queryset = Files.objects.all()
    permission_classes = [IsAdminUser]