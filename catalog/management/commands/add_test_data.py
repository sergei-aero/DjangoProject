from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Очищает базу данных и добавляет тестовые категории и продукты'

    def handle(self, *args, **options):
        # 1. Удаляем все существующие данные
        self.stdout.write('Очистка базы данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Все данные удалены.'))

        # 2. Создаём категории
        self.stdout.write('Создание категорий...')
        electronics = Category.objects.create(
            name='Электроника',
            description='Гаджеты, устройства, компьютеры'
        )
        books = Category.objects.create(
            name='Книги',
            description='Художественная и техническая литература'
        )
        clothes = Category.objects.create(
            name='Одежда',
            description='Мужская, женская, детская'
        )
        self.stdout.write(self.style.SUCCESS(f'Создано {Category.objects.count()} категорий.'))

        # 3. Создаём продукты
        self.stdout.write('Создание продуктов...')
        Product.objects.create(
            name='Смартфон X',
            description='Мощный смартфон с отличной камерой',
            price=29999.99,
            category=electronics
        )
        Product.objects.create(
            name='Ноутбук Pro',
            description='Для работы и игр',
            price=89999.00,
            category=electronics
        )
        Product.objects.create(
            name='Изучаем Django',
            description='Практическое руководство по Django',
            price=1200.00,
            category=books
        )
        Product.objects.create(
            name='Футболка хлопок',
            description='Белая, размер M',
            price=999.99,
            category=clothes
        )
        Product.objects.create(
            name='Наушники Bluetooth',
            description='Беспроводные, шумоподавление',
            price=5499.00,
            category=electronics
        )
        self.stdout.write(self.style.SUCCESS(f'Создано {Product.objects.count()} продуктов.'))

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно добавлены.'))