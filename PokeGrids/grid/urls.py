from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import PokemonViewSet, SubmissionViewSet, PokemonStatisticViewSet

router = DefaultRouter()
router.register(r'pokemon', PokemonViewSet, basename='pokemon')
router.register(r'submission', SubmissionViewSet, basename='submission')
router.register(r'pokemon-statistic', PokemonStatisticViewSet, basename='pokemon-statistic')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/submission-count/<str:date>/', views.get_submission_count, name='submission_count'),
    path('api/pokemon-statistic-count/<int:grid>/<str:pokemon_name>/<str:date>/', views.get_pokemon_statistic_count, name='pokemon_statistic_count'),
]