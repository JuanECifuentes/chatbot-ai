from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Initialize PostgreSQL database with pgvector extension'

    def handle(self, *args, **options):
        self.stdout.write('Enabling pgvector extension...')
        
        with connection.cursor() as cursor:
            cursor.execute('CREATE EXTENSION IF NOT EXISTS vector;')
        
        self.stdout.write(self.style.SUCCESS('✓ pgvector extension enabled successfully!'))
        self.stdout.write('Database is ready for vector operations.')
