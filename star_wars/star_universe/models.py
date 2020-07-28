from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.TextField(blank=True)
    
    
class Staff(models.Model):
    character = 'character'
    director = 'director'
    producer = 'producer'
    CHOICES = (
        (character, 'Character'),
        (director, 'Director'),
        (producer, 'Producer'),
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    type_staff = models.CharField(choices=CHOICES, max_length=20)


class Planet(models.Model):
    name = models.TextField(blank=True)


class Movie(models.Model):
    name = models.TextField(blank=True)
    detail = models.TextField(blank=True)
    planet = models.ManyToManyField(Planet)
    staff = models.ManyToManyField(Staff)
