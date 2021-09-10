from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'phone',
                    'image_tag', 'jdate_joined')
    list_filter = ('date_joined',)
    search_fields = ('first_name', 'last_name', 'email', 'description')
