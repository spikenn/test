import random
from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404

from task.models import User, Record, Status


def random_phone(n=12):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


class Command(BaseCommand):
    help = 'Сгенерировать статусы и рекорды'

    def add_arguments(self, parser):
        parser.add_argument('--records', default=100, type=int, help='Количество рекордов для создания')
        parser.add_argument('--user', default=1, type=int, help='ID пользователя')

    def handle(self, *args, **options):
        status_list = ['success', 'failed', 'not defined', 'suspecious', 'running', 'unknown']

        for status in status_list:
            Status.objects.get_or_create(title=status)
        
        status_list_from_db = Status.objects.all()
        record_list = []
        try:
            user = User.objects.get(id=options['user'])
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('Пользователь с ID "%s" не существует.' % options['user']))
            return

        for _ in range(options['records']):
            record_list.append(
                Record(
                    user=user, status=status_list_from_db[random.randint(0, status_list_from_db.count() - 1)],
                    phone=random_phone(),
                    description='test description'
                )
            )
        
        Record.objects.bulk_create(record_list)

        self.stdout.write(self.style.SUCCESS('Рекорды созданы'))
