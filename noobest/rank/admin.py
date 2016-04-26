from django.contrib import admin
from rank.models import Player


class PlayerAdmin(admin.ModelAdmin):
	list_display = ('id', 'username', 'userid', 'division', 'vector', 'rank', 'recent_match')


admin.site.register(Player, PlayerAdmin)
