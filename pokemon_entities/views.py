import folium
import json
import get_object_or_404

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokePokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now_time = localtime()
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokePokemonEntity.objects.filter(appeared_at__lt=now_time, disappeared_at__gt=now_time)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    now_time = localtime()
    requested_pokemons = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_entities = PokePokemonEntity.objects.filter(pokemon=requested_pokemons, appeared_at__lt=now_time, disappeared_at__gt=now_time)
    pokemon = {
        'img_url': request.build_absolute_uri(requested_pokemons.image.url),
        'title_ru': requested_pokemons.title,
        'title_en': requested_pokemons.title_en,
        'title_jp': requested_pokemons.title_jp,
        'description': requested_pokemons.description,
    }
    prev_evolution = requested_pokemons.previous_evolution
    if prev_evolution:
        pokemon['previous_evolution'] = {
            'img_url': request.build_absolute_uri(prev_evolution.image.url),
            'title_ru': prev_evolution.title,
            'pokemon_id': prev_evolution.id,
        }
    next_evolution = requested_pokemons.next_evolution.first()
    if next_evolution:
        pokemon['next_evolution'] = {
            'img_url': request.build_absolute_uri(next_evolution.image.url),
            'title_ru': next_evolution.title,
            'pokemon_id': next_evolution.id,
        }
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(requested_pokemons.image.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
