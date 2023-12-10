from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import PokemonViewSet, SubmissionViewSet, PokemonStatisticViewSet, ScoreViewSet

router = DefaultRouter()
router.register(r'pokemon', PokemonViewSet, basename='pokemon')
router.register(r'submission', SubmissionViewSet, basename='submission')
router.register(r'pokemon-statistic', PokemonStatisticViewSet, basename='pokemon-statistic')
router.register(r'score', ScoreViewSet, basename='score')

urlpatterns = [
    path('', views.index, name='index'),
    path('create-grid/', views.test_grid, name='create-grid'),
    path('api/', include(router.urls)),
    path('api/pokemon-statistic/<int:grid>/<str:pokemon_name>/<str:date>/', PokemonStatisticViewSet.as_view({'get': 'get_statistic_count'}), name='get-statistic-count'),
    path('api/pokemon-statistic/<int:grid>/<str:date>/', PokemonStatisticViewSet.as_view({'get': 'get_most_submitted'}, name='get-most-submitted')),
    path('api/submission-count/<str:date>/', views.get_submission_count, name='submission_count'),
]