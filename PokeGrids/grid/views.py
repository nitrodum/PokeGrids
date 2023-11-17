from django.shortcuts import render
from django.http import HttpResponse
from .models import Grid, Pokemon
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .serializers import PokemonSerializer

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
    ordering_fields = ['name', 'generation', 'evolution_stage', 'lengendary']
