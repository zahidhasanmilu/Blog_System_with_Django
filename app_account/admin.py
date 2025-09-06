from django.contrib import admin
from .models.managers import CustomUser
from .models.profile import Profile



# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','first_name', 'last_name', 'is_verified')
 
    

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__first_name', 'age','city', 'country', 'mobile', 'user__is_verified')
