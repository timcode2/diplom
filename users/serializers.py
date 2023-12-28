from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def save(self, **kwargs):
        """Сохранение пользователя в базу данных"""

        data = super().save(**kwargs)
        data.set_password(self.validated_data['password'])  # Задание пароля
        data.save()  # Сохранение в базе данных

        return data


class UserFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]
