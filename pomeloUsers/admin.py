from django.contrib import admin
from pomeloUser.models import PomeloUser, Gift

class PomeloUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'user')
	
class GiftAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'price', 'url_video', 'sender', 'receiver')
	
admin.siste.register(PomeloUser, PomeloUserAdmin)
admin.siste.register(Gift, GiftAdmin)
