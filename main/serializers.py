from rest_framework import serializers
from main.models import Files
from users.serializers import UserFilesSerializer


class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания (загрузки документа)"""

    class Meta:
        model = Files
        fields = ['file']


class DocumentListSerializer(serializers.ModelSerializer):
    """Сериализатор для прсмотра отправленных файлов"""
    user = UserFilesSerializer(read_only=True)  # вложенный сериализатор

    class Meta:
        model = Files
        fields = ['id', 'user', 'file', 'status']


class DocumentCheckSerializer(serializers.ModelSerializer):
    """Сериализатор для  админов на принятие или отклонение жокумента"""
    user = UserFilesSerializer(read_only=True)  # вложенный сериализатор

    class Meta:
        model = Files
        fields = ['id', 'status', 'user']


class DocumentIdSerializer(serializers.ModelSerializer):
    """Сериализатор для удаления документов"""
    class Meta:
        model = Files
        fields = ['id']


class DocumentAllSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра данных каждого документа отдельно"""
    user = UserFilesSerializer(read_only=True) # вложенный сериализатор

    class Meta:
        model = Files
        fields = '__all__'
