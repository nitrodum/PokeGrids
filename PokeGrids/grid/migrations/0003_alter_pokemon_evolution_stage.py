# Generated by Django 4.2.7 on 2023-11-14 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0002_alter_pokemon_lengendary_alter_pokemon_type2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='evolution_stage',
            field=models.IntegerField(default=0),
        ),
    ]
