from django.contrib import admin
from main.models import Files
from main.utils import send_approval_notification, send_rejection_notification


@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ("user", "file", "status")

    def save_model(self, request, obj, form, change):
        # Сохраняем изменения в модели
        super().save_model(request, obj, form, change)

        # Проверяем, был ли изменен статус accept_file или denied_file
        if obj.status != 3:
            user_email = obj.user.email

            # Отправляем уведомление в зависимости от статуса
            if obj.status == 1:
                send_approval_notification(user_email)
            elif obj.status == 2:
                send_rejection_notification(user_email)
