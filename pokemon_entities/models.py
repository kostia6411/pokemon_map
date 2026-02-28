from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='наименование покемона')
    image = models.ImageField(null=True, blank=True, upload_to='Pokemon_images/', verbose_name='изображение покемона')

    def __str__(self):
        return f'{self.title}'
    

class PokePokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.SET_DEFAULT, default="default")
    lat = models.FloatField(verbose_name='широта покемона')
    lon = models.FloatField(verbose_name='долгота покемона')
    appeared_at = models.DateTimeField(verbose_name='время появленя покемона')
    disappeared_at = models.DateTimeField(verbose_name='время ухода покемона')
    Level = models.IntegerField(verbose_name='Уровень покемона')
    Health = models.IntegerField(verbose_name='Здоровье покемона')
    Attack = models.IntegerField(verbose_name='Атака покемона')
    Protection = models.IntegerField(verbose_name='Защита покемона')
    Endurance = models.IntegerField(verbose_name='Выносливость покемона')