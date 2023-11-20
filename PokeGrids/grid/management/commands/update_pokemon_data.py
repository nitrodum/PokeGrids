import csv
from django.core.management.base import BaseCommand
from grid.models import Pokemon

class Command(BaseCommand):
    help = "Update Pokemon data with pokedex_number from CSV file"
    
    def handle(self, *args, **options):
        file_path = 'C:\\Users\\nitro\\OneDrive\\Documents\\Projects\\pokedex.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                pokedex_number = int(row['pokedex_number'])
                
                try:
                    pokemon = Pokemon.objects.get(name=name)
                    pokemon.pokedex_number = pokedex_number
                    pokemon.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated pokedex_number for {name}'))
                except Pokemon.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Pokemon with name {name} does not exist, skipping update'))
                except ValueError:
                    self.stdout.write(self.style.ERROR(f'Invalid pokedex_number value for {name}: {row["pokedex_number"]}'))
        self.stdout.write(self.style.SUCCESS('Finished updating Pokemon data'))
