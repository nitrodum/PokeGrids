from django.urls import path, include
from .views import index
from rest_framework.routers import DefaultRouter
from .views import PokemonViewSet

router = DefaultRouter()
router.register(r'api/pokemon', PokemonViewSet, basename='pokemon')

urlpatterns = [
    path('', index, name='index'),
    path('', include(router.urls)),
]