from django.contrib import admin

from .models import Player, FieldPosition, AgeGroup


admin.site.register(AgeGroup)
admin.site.register(FieldPosition)
admin.site.register(Player)
