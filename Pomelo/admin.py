from django.contrib import admin
from models.models import PomeloUser, Gift

class PomeloUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    
class GiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'message', 'url_video', 'sender', 'receiver')
    
admin.site.register(PomeloUser, PomeloUserAdmin)
admin.site.register(Gift, GiftAdmin)
