from django.contrib import admin
from main.models import Files
from main.utils import send_approval_notification, send_rejection_notification


@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'accept_file', 'denied_file')

    def save_model(self, request, obj, form, change):
        # Сохраняем изменения в модели
        super().save_model(request, obj, form, change)

        # Проверяем, был ли изменен статус accept_file или denied_file
        if obj.accept_file or obj.denied_file:
            user_email = obj.user.email

            # Отправляем уведомление в зависимости от статуса
            if obj.accept_file:
                send_approval_notification(user_email)
            elif obj.denied_file:
                send_rejection_notification(user_email)
