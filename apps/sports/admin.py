from django.contrib import admin
from .models import Sport, League, Team, Match

admin.site.register(Sport)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Match)
