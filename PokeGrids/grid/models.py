from django.db import models

# Create your models here.

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    type1 = models.CharField(max_length=50)
    type2 = models.CharField(max_length=50, default="None")
    generation = models.IntegerField()
    evolution_stage = models.IntegerField(default=0)
    lengendary = models.CharField(max_length=50)

class Grid(models.Model):
    selected = models.IntegerField()
    type = models.CharField(max_length=50)
    generation = models.IntegerField()
    evolution_stage = models.IntegerField()
    lengendary = models.BooleanField()