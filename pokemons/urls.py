from django.conf.urls import include, url

from pokemons.views import pokemon_list,menu,ver_pokemon,ver_pokemons_tipo,test

urlpatterns = [
    url(r'^$',menu,name="menu"),
    url(r'^test/$',test,name="test"),
    url(r'^pokemon-list/$',pokemon_list, name="pokemon_list"),
    url(r'^pokemon/(?P<id_pokemon>\d+)/$',ver_pokemon,name="ver_pokemon"),
    url(r'^pokemon-tipo/(?P<id_typo>\d+)/$',ver_pokemons_tipo,name="ver_pokemons_tipo")
]
