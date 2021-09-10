from django.contrib import admin

from .models import SiteSetting, Faq


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'phone', 'address', 'email',
                    'second_logo_tag', 'about_us_image_tag', 
                    'background_image_tag', 'not_found_image_tag']


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'jcreated', 'jupdated']
    search_fields = ('title', 'description')
