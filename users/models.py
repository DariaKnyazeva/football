from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.utils import timezone


class UserRole:
    COACH = 1
    PLAYER = 2


class UserManager(DjangoUserManager):
    def create_user(self, username, user_role=UserRole.COACH, email=None, password=None):
        """
        Creates and saves a User with the given username, email and password.
        By default creates Coach user
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now)

        user.set_password(password)
        user.user_role = user_role
        user.save(using=self._db)
        return user

    def create_coach(self, username, email=None, password=None):
        return self.create_user(username, email=email, password=password)

    def create_player(self, username, email=None, password=None):
        return self.create_user(username, user_role=UserRole.PLAYER, email=email, password=password)

    def _create_user(self, username, email, password, user_role=UserRole.COACH, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        By default creates Coach user
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, user_role=user_role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    USER_ROLE_CHOICES = (
        (UserRole.COACH, 'Coach'),
        (UserRole.PLAYER, 'Player'),
    )
    user_role = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES)

    objects = UserManager()

    @property
    def is_coach(self):
        return self.user_role == UserRole.COACH
