from django.urls import path

from main.apps import MainConfig
from main.views import (
    DocumentCreateAPIView,
    DocumentAPIView,
    DocumentUpdateAPIView,
    DocumentDestroyAPIView,
    DocumentRetrieveAPIView,
)


app_name = MainConfig.name

urlpatterns = [
    path(
        "create/", DocumentCreateAPIView.as_view(), name="create"
    ),  # загрузка документа
    path(
        "", DocumentAPIView.as_view(), name="files"
    ),  # просмотр всех отправленных документов
    path("<int:pk>/update/", DocumentUpdateAPIView.as_view(), name="update_file"),
    path("<int:pk>/delete/", DocumentDestroyAPIView.as_view(), name="delete"),
    path("<int:pk>/detail/", DocumentRetrieveAPIView.as_view(), name="detail_file"),
]
