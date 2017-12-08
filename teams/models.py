# -*- coding: utf-8 -*-
from django.db import models


class Team(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    coach = models.ForeignKey('users.User')
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.ForeignKey('players.AgeGroup')
    country = models.CharField(max_length=255, default='United Kingdom')
    city = models.CharField(max_length=255, default='London')
    address = models.CharField(max_length=255, blank=True, default='')

    players = models.ManyToManyField('players.Player', null=True, blank=True)
    side_players = models.ManyToManyField('players.Player', null=True, blank=True, related_name='side_players')

    def __str__(self):
        return self.name
