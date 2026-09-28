"""Management command для создания базы данных MS SQL."""
import pyodbc
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """Создаёт базу данных MS SQL, если её нет."""

    help = 'Создаёт базу данных MS SQL, указанную в настройках.'

    def handle(self, *args, **options):
        """Создаёт БД через подключение к master."""
        db_config = settings.DATABASES['default']
        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config['HOST']
        db_port = db_config.get('PORT') or ''

        # Формируем SERVER — либо host,port, либо только host (для именованных экземпляров)
        if db_port:
            server = f'{db_host},{db_port}'
        else:
            server = db_host

        # Экранируем обратные слэши для строки подключения
        server = server.replace('\\', '\\\\')

        conn_str = (
            'DRIVER={ODBC Driver 18 for SQL Server};'
            f'SERVER={server};'
            'DATABASE=master;'
            f'UID={db_user};'
            f'PWD={db_password};'
            'TrustServerCertificate=yes;'
        )

        self.stdout.write(f'Подключение к MS SQL ({server})...')

        try:
            conn = pyodbc.connect(conn_str, autocommit=True)
        except pyodbc.Error as e:
            raise CommandError(f'Не удалось подключиться к MS SQL: {e}')

        cursor = conn.cursor()

        cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{db_name}'")
        exists = cursor.fetchone()

        if exists:
            self.stdout.write(self.style.WARNING(f'База "{db_name}" уже существует.'))
        else:
            cursor.execute(f'CREATE DATABASE [{db_name}]')
            self.stdout.write(self.style.SUCCESS(f'База "{db_name}" создана.'))

        cursor.close()
        conn.close()
        self.stdout.write(self.style.SUCCESS('Готово.'))
