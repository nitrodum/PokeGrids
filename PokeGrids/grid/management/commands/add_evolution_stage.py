import csv
import requests
from django.core.management.base import BaseCommand
from grid.models import Pokemon

class Command(BaseCommand):
    help = 'Add evolution_stage to the existing CSV data'

    def handle(self, *args, **options):
        # Function to fetch evolution stage from Pokédex API
        

        # Read the existing data from the model (assuming you have a Django model for this CSV data)
        queryset = Pokemon.objects.all().order_by('id')
        updated_data = []

        # Add evolution_stage to the model and update the list
        for instance in queryset:
            # Prepare a dictionary with updated data
            updated_data.append({
                'pokedex_number': instance.pokedex_number,
                'name': instance.name,
                'generation': instance.generation,
                'evolution_stage': instance.evolution_stage,
                'status': instance.legendary,
                'type_1': instance.type1,
                'type_2': instance.type2,
            })

        # Write the updated data to the CSV file
        csv_file_path = '/home/nitrodum/djangoproject/PokeGrids/pokedex.csv'  # Replace with the actual path to your CSV file
        fieldnames = ['pokedex_number', 'name', 'generation', 'evolution_stage', 'status', 'type_1', 'type_2']

        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()

            # Write data
            for data in updated_data:
                writer.writerow(data)

        self.stdout.write(self.style.SUCCESS('Evolution stages added and CSV file updated successfully.'))