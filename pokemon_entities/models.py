from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name='наименование покемона')
    image = models.ImageField(null=True, blank=True, upload_to='Pokemon_images/', verbose_name='изображение покемона')
    description = models.CharField(max_length=200, blank=True, verbose_name='описание покемона')

    def __str__(self):
        return f'{self.title}'
    

class PokePokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='ссылка на покемона', related_name='entities', blank=True, null=True)
    lat = models.FloatField(verbose_name='широта покемона', blank=True, null=True)
    lon = models.FloatField(verbose_name='долгота покемона', blank=True, null=True)
    appeared_at = models.DateTimeField(verbose_name='время появления покемона', blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name='время исчезновения покемона', blank=True, null=True)
    level = models.IntegerField(verbose_name='Уровень покемона', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье покемона', blank=True, null=True)
    attack = models.IntegerField(verbose_name='Атака покемона', blank=True, null=True)
    protection = models.IntegerField(verbose_name='Защита покемона', blank=True, null=True)
    endurance = models.IntegerField(verbose_name='Выносливость покемона', blank=True, null=True)