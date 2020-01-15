from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404

import requests

def menu(request):
    return render(request,'menu.html')
def test(request):
    return render(request,'test.html')

def pokemon_list(request):
    offset=0
    url = 'https://pokeapi.co/api/v2/pokemon/?limit=10'
    args = {'offset':offset} if offset else {}
    response = requests.get(url,params=args)

    estructura = {}
    contenido = {}
    idPokemon = 0
    if response.status_code == 200:
        payload = response.json()
        results = payload.get('results',[])

        if results:
            for pokemon in results:
                idPokemon = idPokemon + 1
                name = pokemon['name']
                image = get_image_pokemon(pokemon['url'])
                image1 =image.get('image')
                #print("image pokemon:"+pokemon['url'])
                estructura[name] = {
                    'id': idPokemon ,
                    'nombre':name,
                    'url': pokemon['url'],
                    'image': image1,
                }
    return render(request,'pokemon_list.html',{'Pokemons':estructura})

def get_image_pokemon(url):
    response = requests.get(url)

    if response.status_code == 200:
        response_json = response.json()
        sprite = response_json['sprites']
        idPokemon = response_json['id']
        data = {}
        data = {
            'image':sprite['front_default'],
            'idPokemon': idPokemon,
        }
        return data
def pokemon_number_pokedex(url):
    response = requests.get(url)

    if response.status_code == 200:
        response_json = response.json()
        idPokemon = response_json['id']
        return idPokemon

def ver_pokemon(request,id_pokemon):
    url = 'https://pokeapi.co/api/v2/pokemon/'+ str(id_pokemon)
    detalles = detalles_caracteristicas(url)
    
    name = detalles.get('name')
    peso = detalles.get('weight')
    altura = detalles.get('height')
    sprites = get_image_pokemon(url)
    image = sprites.get('image')
    types = detalles.get('types')
    habilidad = detalles.get('abilities')
    moves = detalles.get('moves')

    totalmoves = []
    totalHabilidad = []
    totaltypes = []

    for ntypespokemon in types:
        provisional = ntypespokemon['type']
        nametype = provisional['name']
        urltype = provisional['url']
        
        if urltype[32] =='/':
            idtypo=urltype[31]
        else:
            idtypo=urltype[31]+urltype[32]


        diccionarioType = {'name':nametype,'url':urltype,'idtypo':idtypo}

        totaltypes.append(diccionarioType)
        

    for nHabilidad in habilidad:
        Hprob = nHabilidad['ability']
        nameHabilidad = Hprob['name']
        
        totalHabilidad.append(nameHabilidad)

    for nmoves in moves:
        Mprob = nmoves['move']
        nameMove = Mprob['name']

        totalmoves.append(nameMove)

    caracteristicas = {}
    print(totaltypes)
    caracteristicas = {
        'nombre':name,
        'peso':peso,
        'altura':altura,
        'sprites':image,
        'types':totaltypes,
        'Habilidad':totalHabilidad,
        'moves':totalmoves,
    }

    return render(request,'pokemon_perfil.html',{'caracteristicas':caracteristicas})

def detalles_caracteristicas(url):
    response = requests.get(url)

    if response.status_code == 200:
        response_json = response.json()
        return response_json

def ver_pokemons_tipo(request,id_typo):
    url = 'https://pokeapi.co/api/v2/type/'+str(id_typo)
    response = requests.get(url)
    totalPokemonsType = {}
    cantidad = 0
    if response.status_code == 200:
        response_json = response.json()
        payload = response.json()
        results = payload.get('pokemon')
        if results:
            for pokemon in results:
                pokemonprov = pokemon['pokemon']
                namePokemon = pokemonprov['name']
                urlpokemon = pokemonprov['url']
                imagen = get_image_pokemon(urlpokemon)
                imagen1 = imagen.get('image')
                idPokemon = imagen.get('idPokemon')
                totalPokemonsType[namePokemon]={
                    'nombre':namePokemon,
                    'image':imagen1,
                    'id':idPokemon,
                    'url':urlpokemon
                }
                cantidad = cantidad+1
                if cantidad == 9:
                    break 
    return render(request,'pokemon_list.html',{'Pokemons':totalPokemonsType})
        