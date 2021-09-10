from django.contrib import admin

from .models import ContactUs


@admin.register(ContactUs)
class ContactUs(admin.ModelAdmin):
	list_display = ['name', 'subject', 'message', 'email', 'phone', 
					'jcreated', 'reviewed']
	list_filter = ('created', 'reviewed')
	search_fields = ('name', 'email', 'phone', 'subject',)
