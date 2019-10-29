from .models import Pokemon

class PokemonSerializer(serializer.ModelSerializer):
	class Meta:
		model = Pokemon
		feilds = ['pokemon_id', 'name', 'sprites', 'type1', 'type2']
