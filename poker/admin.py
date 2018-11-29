from django.contrib import admin
from poker.models import Table, Player, Hand

# Register your models here.
admin.site.register(Table)
admin.site.register(Player)
admin.site.register(Hand)