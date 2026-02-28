from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='наименование покемона')
    image = models.ImageField(null=True, blank=True, upload_to='Pokemon_images/', verbose_name='изображение покемона')

    def __str__(self):
        return f'{self.title}'
    

class PokePokemonEntity(models.Model):
    lat = models.FloatField(verbose_name='широта покемона')
    lon = models.FloatField(verbose_name='долгота покемона')