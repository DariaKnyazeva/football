from django.db import models


class AgeGroup(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FieldPosition(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Player(models.Model):
    """
    Holds the Player info
    """
    class Salutation:
        MISTER = 'Mr.'
        MISSIS = 'Mrs.'
        MISSIS_SHORT = 'Ms.'
        MISS = 'Miss.'

    SALUTATION_CHOICES = (
        (Salutation.MISTER, Salutation.MISTER),
        (Salutation.MISSIS, Salutation.MISSIS),
        (Salutation.MISSIS_SHORT, Salutation.MISSIS_SHORT),
        (Salutation.MISS, Salutation.MISS),
    )

    registration_date = models.DateField(auto_now_add=True)
    salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    parent_first_name = models.CharField(max_length=255)
    parent_last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField()
    age_group = models.ManyToManyField(AgeGroup, null=True, blank=True)
    field_position = models.ManyToManyField(FieldPosition, null=True, blank=True)

    # TODO: mobile
    # TODO: trial dates

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def gender(self):
        if self.salutation == Player.Salutation.MISTER:
            return 'M'
        return 'F'
