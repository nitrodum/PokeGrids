from django.shortcuts import render
from django.http import HttpResponse
from .models import Grid

# Create your views here.
def index(request):

    grid_data = Grid.objects.all()

    return render(request, 'index.html', {"grid_data":grid_data})
