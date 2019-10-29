from django.urls import path
# from .views import PokemonView
from . import views

urlpatterns = [
    # path('', PokemonView.as_view(), name='get_pokemon_app-view_pokemon'),
    path('', views.view_pokemon, name='get_pokemon_app-view_pokemon'),
    path(r'^stats/(?P<pokemon_id>\d+)/$', views.pokemon_stats, name='get_pokemon_app-pokemon_stats'),
]
