import csv
from django.core.management.base import BaseCommand
from grid.models import Pokemon

class Command(BaseCommand):
    help = "Import Pokemon data from CSV file"
    
    def handle(self, *args, **options):
        file_path = 'C:\\Users\\nitro\\OneDrive\\Documents\\Projects\\pokedex.csv'        
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Pokemon.objects.create(
                    pokedex_number=int(row['pokedex_number']),
                    name=row['name'],
                    type1=row['type_1'],
                    type2=row['type_2'],
                    generation=row['generation'],
                    legendary=row['status'],
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported Pokemon data'))
