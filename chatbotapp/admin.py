from django.contrib import admin
from .models import Chat
from .models import UserProfile

# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'response', 'timestamp')
    list_filter = ('user',)
    search_fields = ('message', 'response')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)               
    search_fields = ('user__username',)      


admin.site.register(Chat, ChatAdmin)  
admin.site.register(UserProfile,UserProfileAdmin)