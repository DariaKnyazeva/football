from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class UserRole:
        COACH = 1
        PLAYER = 2

    USER_ROLE_CHOICES = (
        (UserRole.COACH, 'Coach'),
        (UserRole.PLAYER, 'Player'),
    )
    user_role = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES)
