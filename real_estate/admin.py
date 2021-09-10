from django.contrib import admin

from .models import City, Estate, EstateImage


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class EstateImageInline(admin.StackedInline):
    model = EstateImage


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ('title', 'agent', 'status', 'city', 'published_status', 
                    'size', 'price', 'monthly_rent', 'room', 'year', 'floor', 
                    'elevator', 'parking', 'warehouse', 'jcreated', 'jupdated',
                    'link_tag')
    list_filter = ('created', 'published_status')
    list_editable = ('published_status',)
    search_fields = ('title', 'description', 'city__name', 
                     'agent__first_name',)
    raw_id_fields = ('agent',)
    inlines = [EstateImageInline]
