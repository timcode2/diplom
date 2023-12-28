from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            user = User.objects.create(email='artem.matrashov@yandex.ru',
                                       first_name='Artem',
                                       last_name='Matrashov',
                                       is_staff=True,
                                       is_superuser=True)

            user.set_password('admin')
            user.save()

        except IntegrityError as e:
            print('Такой пользователь уже есть')