from django.contrib import admin
from app.models import UserDetails, Role
# Register your models here.
class UserDetailsAdmin(admin.ModelAdmin):
        list_display = ('id','user', 'role',) 
        list_filter = ('user','role')
        search_fields = ('user', 'role',) 

admin.site.register(UserDetails, UserDetailsAdmin)

class RoleAdmin(admin.ModelAdmin):
        list_display = ('id','role',)
        search_fields = ('role',)

admin.site.register(Role, RoleAdmin)