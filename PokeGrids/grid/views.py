import random
from datetime import timedelta
#from celery import Celery
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import Grid, Pokemon, Submission, PokemonStatistic, Score, ArchivedGrid
from .serializers import PokemonSerializer, SubmissionSerializer, PokemonStatisticSerializer, ScoreSerializer

#celery_app = Celery('PokeGrids')

# Create your views here.
def index(request):
    grid_data = Grid.objects.all()
    return render(request, 'index.html', {"grid_data":grid_data})

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

class PokemonPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100 

class PokemonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    pagination_class = PokemonPagination
    search_fields = ['name']
    ordering_fields = ['id','name', 'generation', 'evolution_stage', 'legendary']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_input = self.request.GET.get('search', None)

        if search_input:
            # Split the search input into words
            search_terms = search_input.split()

            # Use Q objects to create a complex query for partial word matching
            query = Q()
            for term in search_terms:
                # First, try to match names that start with the term
                query |= Q(name__istartswith=term)
                # If no exact matches, use regex to match anywhere in the name
                query |= Q(name__iregex=r'\y{}\y'.format(term))

            queryset = queryset.filter(query)

        return queryset

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

class PokemonStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PokemonStatistic.objects.all()
    serializer_class = PokemonStatisticSerializer
    ordering_fields = ['']

    @action(detail=False, methods=['get'])
    def get_statistic_count(self, request, grid, pokemon_name, date):
        try:
            statistic = PokemonStatistic.objects.filter(grid=grid, pokemon__name=pokemon_name, date=date).first()
            if statistic is None:
                count = 0
            else: count = statistic.submission_count
            return Response({'count': count})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    @action(detail=False, methods=['get'])
    def get_most_submitted(self, request, grid, date):
        try:
            mostSubmittedPokemon = PokemonStatistic.objects.filter(grid=grid, date=date).order_by('-submission_count').first()
            serializer = self.get_serializer(mostSubmittedPokemon)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

def get_submission_count(request, date):
    try:
        count = Submission.objects.filter(date=date).count()
        return JsonResponse({'count': count})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)   

def archive_current_grid():
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    current_grid_data = get_current_grid_data(yesterday)
    ArchivedGrid.objects.create(date=yesterday, grid_data=current_grid_data)
    Grid.objects.all().delete()
    create_grid()
    last_three_archived_grids = ArchivedGrid.objects.all().order_by('-date')[:3]
    last_three_grid_data = [archived_grid.grid_data for archived_grid in last_three_archived_grids]
    current_grid_data = get_current_grid_data(getDate())
    isGridValid = checkGrid(current_grid_data,last_three_grid_data)
    while (not isGridValid):
        Grid.objects.all().delete()
        create_grid()
        current_grid_data = get_current_grid_data(getDate())
        isGridValid = checkGrid(current_grid_data,last_three_grid_data)

    return HttpResponse("Archiving the current grid. This may take some time.", current_grid_data)

def checkGrid(current_grid_data,last_three_grid_data):
    for i in range (0,6):
        current_grid_item = current_grid_data[i] 
        for last_three_grid_item in last_three_grid_data:
            if current_grid_item in last_three_grid_item[:3]:
                if i < 3:
                    for j in range(3,6):
                        if current_grid_data[j] in last_three_grid_item[3:6]:
                            return False
                else:
                    for j in range(0,3):
                        if current_grid_data[j] in last_three_grid_item[3:6]:
                            return False
    return True


def get_current_grid_data(date):
    current_grid_data = []

    grid_items = Grid.objects.filter(date=date)

    for grid_item in grid_items:
        # Use grid_item attributes to fetch corresponding Pokemon data
        grid_data = {
            'selected': grid_item.selected,
            'type': grid_item.type,
            'generation': grid_item.generation,
            'evolution_stage': grid_item.evolution_stage,
            'legendary': grid_item.legendary
        }
        current_grid_data.append(grid_data)

    return current_grid_data
def test_grid(request):
    archive_current_grid()
    return HttpResponse(timezone.now())
def create_grid():
    selectors = [1,2,3,4]
    rowSelectorWeights = [16,1,1,1]
    colSelectorWeights = [16,1,1,1]
    types = ['normal', 'fire', 'water', 'grass', 'electric', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy', 'Mono', 'Dual']
    random.shuffle(types)
    usedRowTypes = []
    usedColTypes = []
    baseGenertion = 1
    baseStage = 1

    for i in range(6):
        if i < 3:
            selector = random.choices(selectors, weights=rowSelectorWeights, k=1)[0]
            rowSelectorWeights[0] = max(1, rowSelectorWeights[0] // 2)
            if selector == 1:
                Grid.objects.create(
                    selected = selector,
                    type = types[i], 
                    date = getDate()
                )
                usedRowTypes.append(types[i])
                types.remove(types[i])
            elif selector == 2:
                randomGen = random.randint(baseGenertion,8)
                if randomGen == 8:
                    rowSelectorWeights[1] = 0
                else:
                    baseGenertion = randomGen + 1
                Grid.objects.create(
                    selected = selector,
                    generation = randomGen,
                    date = getDate()
                )
                rowSelectorWeights[0] = 0
                colSelectorWeights[1] = 0
            elif selector == 3:
                randomStage = random.randint(baseStage,3)
                if randomStage == 3:
                    rowSelectorWeights[2] = 0
                else:
                    baseStage = randomStage + 1
                Grid.objects.create(
                    selected = selector,
                    evolution_stage = randomStage,
                    date = getDate()
                )
                rowSelectorWeights[0] = 0
                colSelectorWeights[2] = 0
                colSelectorWeights[3] = 0
            else:
                Grid.objects.create(
                    selected = selector,
                    legendary = True,
                    date = getDate()
                )
                rowSelectorWeights[0] = 0
                rowSelectorWeights[3] = 0
                colSelectorWeights[2] = 0
                colSelectorWeights[3] = 0
        else:
            selector = random.choices(selectors, weights=colSelectorWeights, k=1)[0]
            colSelectorWeights[0] = int(colSelectorWeights[0]/2)
            if selector == 1:
                if 'Mono' in usedRowTypes or 'Dual' in usedRowTypes:
                    types = list(set(types) - {'Mono', 'Dual'})
                while any(check_invalid_combination(types[i], usedType) for usedType in usedRowTypes):
                    if len(types) > 0:
                        types.remove(types[i])
                Grid.objects.create(
                    selected = selector,
                    type = types[i],
                    date = getDate()
                )
                usedColTypes.append(types[i])
                types.remove(types[i])
            elif selector == 2:
                randomGen = random.randint(baseGenertion,8)
                if randomGen == 8:
                    colSelectorWeights[1] = 0
                else:
                    baseGenertion = randomGen + 1
                Grid.objects.create(
                    selected = selector,
                    generation = randomGen,
                    date = getDate()
                )
                colSelectorWeights[0] = 0
            elif selector == 3:
                randomStage = random.randint(baseStage,3)
                if randomStage == 3:
                    colSelectorWeights[2] = 0
                else:
                    baseStage = randomStage + 1
                Grid.objects.create(
                    selected = selector,
                    evolution_stage = randomStage,
                    date = getDate()
                )
                colSelectorWeights[0] = 0
            else:
                Grid.objects.create(
                    selected = selector,
                    legendary = True,
                    date = getDate()
                )
                colSelectorWeights[0] = 0
                colSelectorWeights[3] = 0

def check_invalid_combination(type1, type2):
    invalidCombinations = {
        ('normal', 'ice'), ('normal', 'bug'), ('normal', 'rock'), ('normal', 'steel'), ('fire', 'fairy'),
        ('ice', 'poison'), ('ground', 'fairy'), ('bug', 'dragon'),
        ('rock', 'ghost'), ('normal', 'water'), ('fire', 'normal'), ('fire', 'water'), ('fire', 'steel'),
        ('water', 'steel'), ('grass', 'ice'), ('electric', 'normal'),
        ('electric', 'ghost'), ('electric', 'fire'), ('electric', 'psychic'), ('electric', 'dark'),
        ('electric', 'poison'), ('ice', 'ghost'), ('ice', 'ground'), ('ice', 'bug'),
        ('ice', 'steel'), ('ice', 'fairy'), ('ice', 'fire'), ('fighting', 'ice'),
        ('poison', 'normal'), ('poison', 'flying'), ('ground', 'psychic'), ('bug', 'ghost'),
        ('bug', 'fairy'), ('bug', 'dark'), ('rock', 'dark'), ('rock', 'fighting'),
        ('rock', 'dragon'), ('ghost', 'poison'), ('dragon', 'fairy'), ('dark', 'steel'),
        ('dark', 'fairy'), ('steel', 'poison'), ('fairy', 'fighting')
    }

    return (type1, type2) in invalidCombinations or (type2, type1) in invalidCombinations


def getDate():
    date = timezone.now().strftime('%Y-%m-%d')
    return date

# def schedule_next_task():
#     from .tasks import archive_current_grid_task
#     from celery.utils.log import get_task_logger
#     logger = get_task_logger(__name__)
#     logger.info("Scheduling the next task.")
#     result = archive_current_grid_task.apply_async(countdown=24 * 60 * 60)
#     logger.info(f"Next task scheduled. Result ID: {result.id}")
