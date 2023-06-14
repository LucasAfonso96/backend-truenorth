from django.core.management.base import BaseCommand
from calculator.models import Operation

class Command(BaseCommand):
    help = 'Populate initial operations'

    def handle(self, *args, **options):
        operations = [
            {'type': 'addition', 'cost': 0.1},
            {'type': 'subtraction', 'cost': 0.2},
            {'type': 'multiplication', 'cost': 0.3},
            {'type': 'division', 'cost': 0.4},
            {'type': 'square_root', 'cost': 0.5},
            {'type': 'random_string', 'cost': 0.6},
        ]

        for operation in operations:
            Operation.objects.create(type=operation['type'], cost=operation['cost'])

        self.stdout.write(self.style.SUCCESS('Operations successfully populated.'))
