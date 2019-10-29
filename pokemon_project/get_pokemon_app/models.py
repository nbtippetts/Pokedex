from django.db import models

class Pokemon(models.Model):
	pokemon_id = models.IntegerField()
	name = models.CharField(max_length=30)
	sprites = models.CharField(max_length=100)
	type1 = models.TextField()
	type2 = models.TextField()

	def __str__(self):
	 return self.name
