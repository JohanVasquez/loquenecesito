from django.db import models

# Create your models here.
class Character(models.Model):
    name = models.TextField(blank=True)


class Planet(models.Model):
    name = models.TextField(blank=True)


class Movie(models.Model):
    name = models.TextField(blank=True)
    detail = models.TextField(blank=True)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    character = models.ManyToManyField(Character)
    director = models.TextField(blank=True)
    producers = models.TextField(blank=True)
