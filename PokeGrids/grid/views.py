from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from .models import Grid, Pokemon, Submission, PokemonStatistic, Score
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import PokemonSerializer, SubmissionSerializer, PokemonStatisticSerializer, ScoreSerializer

# Create your views here.
def index(request):
    grid_data = Grid.objects.all()
    return render(request, 'index.html', {"grid_data":grid_data})

class PokemonPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100 

class PokemonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    pagination_class = PokemonPagination
    search_fields = ['^name']
    ordering_fields = ['name', 'generation', 'evolution_stage', 'legendary']

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        # Call the parent perform_create method to save the submission
        submission = serializer.save()

        # Extract the date component from the timestamp and update the submission date
        submission.date = submission.timestamp.date()
        submission.save()
        
         # Check if a PokemonStatistics instance already exists for the given grid, Pokemon, and date
        pokemon_statistic, created = PokemonStatistic.objects.get_or_create(
            grid=submission.grid,
            pokemon=submission.pokemon,
            date = submission.date,
            defaults={'submission_count': 1}  # Set the default value if creating a new instance
        )

        # If the PokemonStatistics instance already exists, increment the submission_count by 1
        if not created:
            pokemon_statistic.submission_count += 1
            pokemon_statistic.save()

        # Return a response with the serialized submission
        return Response(serializer.data)

class PokemonStatisticViewSet(viewsets.ModelViewSet):
    queryset = PokemonStatistic.objects.all()
    serializer_class = PokemonStatisticSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

def get_submission_count(request, date):
    try:
        count = Submission.objects.filter(date=date).count()
        return JsonResponse({'count': count})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)   

def get_pokemon_statistic_count(request, grid, pokemon_name, date):
    try:
        count = PokemonStatistic.objects.filter(grid=grid, pokemon__name=pokemon_name, date=date).first().submission_count
        return JsonResponse({'count': count})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
