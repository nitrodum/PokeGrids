from rest_framework import serializers
from .models import Pokemon, Submission, PokemonStatistic, Score, ArchivedGrid

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class PokemonStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonStatistic
        fields = '__all__'
        depth = 1

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

class ArchivedGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivedGrid
        fields = '__all__'
        depth = 1