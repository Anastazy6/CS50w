import django
from django.contrib import admin
from .models import *

class FollowerAdmin(admin.ModelAdmin):
    lsit_display = ('following', 'followed')

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'body', 'timestamp')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',\
                    'date_joined', 'last_login', 'is_active',\
                    'is_staff', 'is_superuser')

# Register your models here.
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Post,     PostAdmin)
admin.site.register(User,     UserAdmin)