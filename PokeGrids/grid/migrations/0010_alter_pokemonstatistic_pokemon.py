# Generated by Django 4.2.7 on 2023-11-19 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0009_rename_pokemonstatistics_pokemonstatistic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonstatistic',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grid.pokemon', to_field='name'),
        ),
    ]
