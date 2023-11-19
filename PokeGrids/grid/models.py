from django.db import models

# Create your models here.

class Pokemon(models.Model):
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
    type = models.CharField(max_length=50)
    generation = models.IntegerField()
    evolution_stage = models.IntegerField()
    legendary = models.BooleanField()
    date = models.DateField()

class Submission(models.Model):
    grid = models.IntegerField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, to_field='name')
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    

class PokemonStatistic(models.Model):
    grid = models.IntegerField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, to_field='name')
    date = models.DateField()
    submission_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['pokemon', 'grid', 'date']
