import json

from django.core.management.base import BaseCommand, CommandError
from books.models import Book


class Command(BaseCommand):
    help = 'Загружает книги из JSON-файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str
        )

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                books = json.load(f)
                for book in books:
                    fields = book.get('fields', {})
                    Book.objects.create(
                        name=fields.get('name', ''),
                        author=fields.get('author', ''),
                        pub_date=fields.get('pub_date')
                    )
        except:
            raise CommandError(f'Возникал ошибка при обработке: {file_path}')

