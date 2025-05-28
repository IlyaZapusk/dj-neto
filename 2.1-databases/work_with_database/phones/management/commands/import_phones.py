import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Импорт телефонов из CSV-файла'

    def add_arguments(self, parser):
        # Здесь можно добавить опции, если нужно
        pass

    def handle(self, *args, **options):
        # Учитываем структуру: файл phones.csv лежит в корне проекта
        csv_path = os.path.join(settings.BASE_DIR, 'phones.csv')

        with open(csv_path, 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            Phone.objects.update_or_create(
                id=phone['id'],
                defaults={
                    'name': phone['name'],
                    'price': phone['price'],
                    'image': phone['image'],
                    'release_date': datetime.strptime(phone['release_date'], '%Y-%m-%d'),
                    'lte_exists': phone['lte_exists'].lower() == 'true',
                    'slug': slugify(phone['name']),
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Импортировано телефонов: {len(phones)}'))
