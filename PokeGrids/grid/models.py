from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Pokemon(models.Model):
    pokedex_number = models.CharField(max_length=20, default='0')  
    name = models.CharField(max_length=100, unique=True)
    type1 = models.CharField(max_length=50)
    type2 = models.CharField(max_length=50, default="None")
    generation = models.IntegerField()
    evolution_stage = models.IntegerField(default=0)
    legendary = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Grid(models.Model):
    selected = models.IntegerField()
    type = models.CharField(max_length=50, default='')
    generation = models.IntegerField(default=0)
    evolution_stage = models.IntegerField(default=0)
    legendary = models.BooleanField(default=False)
    date = models.DateField()

class ArchivedGrid(models.Model):
    date = models.DateField(unique=True, db_index=True)
    grid_data = ArrayField(models.CharField(max_length=100), size=9)

class Submission(models.Model):
    grid = models.IntegerField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, to_field='name')
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(db_index=True)
    

class PokemonStatistic(models.Model):
    grid = models.IntegerField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, to_field='name')
    date = models.DateField(db_index=True)
    submission_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['pokemon', 'grid', 'date']

class Score(models.Model):
    score = models.FloatField()
    date = models.DateField()