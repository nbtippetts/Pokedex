from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http import HttpResponse
from .models import Pokemon
import requests
import requests_cache
import json
# from PIL import Image
# from io import BytesIO

requests_cache.install_cache('pokemon_cache')

# @login_required
def view_pokemon(request):
	if request.method == "POST":
		search_pokemon = request.POST.get('search_box', None)
		if search_pokemon is not None and search_pokemon != '':
			print(search_pokemon)
			context = get_pokemon(search_pokemon)
			return render(request, 'get_pokemon_app/view_pokemon.html', context)
		elif search_pokemon == '':
			context = get_pokemon(search_pokemon=None)
			return render(request, 'get_pokemon_app/view_pokemon.html', context)
		else:
			context = get_pokemon(search_pokemon=None)
			return render(request, 'get_pokemon_app/view_pokemon.html', context)
	else:
		context = get_pokemon(search_pokemon=None)
		return render(request, 'get_pokemon_app/view_pokemon.html', context)

# def size_image(url):
# 	response = requests.get(url)
# 	img = Image.open(BytesIO(response.content))
# 	if img.height > 300 or img.width > 300:
# 		output_size = (250, 250)
# 		img.thumbnail(output_size)
# 		img.save(self.image.path)

def pokemon_stats(request, pokemon_id=None):
	if request.method == "POST":
		search_pokemon = request.POST.get('search_box', None)
		if search_pokemon is not None and search_pokemon != '':
			context = get_pokemon(search_pokemon)
			return render(request, 'get_pokemon_app/pokemon_stats.html', context)
	else:
		context = get_pokemon(pokemon_id)
		return render(request, 'get_pokemon_app/pokemon_stats.html', context)

def get_pokemon(search_pokemon):
	pokemon_list = []
	pokemon = []
	if search_pokemon is None:
		for i in range(1, 10):
			res = requests.get('https://pokeapi.co/api/v2/pokemon/{}/'.format(i))
			pokemon.append(res.json())
	else:
		res = requests.get('https://pokeapi.co/api/v2/pokemon/{}/'.format(search_pokemon))
		pokemon_detail_dict = res.json()
		res1 = requests.get('https://pokeapi.co/api/v2/type/{}/'.format(search_pokemon))
		pokemon_detail_dict.update(res1.json())
		pokemon.append(pokemon_detail_dict)

	for poke in pokemon:
		pokemon_dict = {}
		for k, p in poke.items():
			if 'species' in k:
				pokemon_dict.setdefault(k,p['name'])
			if 'sprites' in k:
				pokemon_dict.setdefault(k,p['front_default'])
			elif 'types' in k:
				count = 0
				for sub_p in p:
					pokemon_dict.setdefault('{0}{1}'.format(k, count),sub_p['type']['name'])
					count += 1
			elif 'id' in k:
				pokemon_dict.setdefault(k,p)
			elif 'height' in k:
				convert_height=p/3.048
				print(convert_height)
				pokemon_dict.setdefault(k, convert_height)
			elif 'weight' in k:
				convert_weight = p/4.536
				print(convert_weight)
				pokemon_dict.setdefault(k, convert_weight)
			elif 'stats' in k:
				for sub_p in p:
					if 'special-attack' in sub_p['stat']['name']:
						sub_p['stat']['name'] = 'special_attack'
					if 'special-defense' in sub_p['stat']['name']:
						sub_p['stat']['name'] = 'special_defense'
					pokemon_dict.setdefault(sub_p['stat']['name'], sub_p['base_stat'])
			elif 'damage_relations' in k:
				for sub_p in p['double_damage_from']:
					pokemon_dict.setdefault("weakness",[]).append(sub_p['name'])
			else:
				pokemon_dict.setdefault(k, p)
		pokemon_list.append(pokemon_dict)
	# Pokemon height formula - divide the length value by 3.048
	# Pokemon weight formula - divide the mass value by 4.536
	# Pokemon Stats - hp, attack, defense, special attack, special defence, speed
	# Pokemon Weaknesses
	context = {
		'pokemon': pokemon_list
	}

	return context
