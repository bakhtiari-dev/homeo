from django.contrib import admin

from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'estate_count', 'day_count', 'price')
    search_fields = ('name', 'estate_count', 'day_count', 'price')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('agent', 'name', 'price', 'jcreated', 'day_count', 
                    'estate_count', 'created_estates', 'jexpiration_date', 
                    'active')
    search_fields = ('agent', 'name', 'price', 'day_count', 'estate_count', 
                     'created_estates', 'created')
    raw_id_fields = ('agent',)
