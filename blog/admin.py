from django.contrib import admin
from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title',)
	search_fields = ('title',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ['author', 'title', 'published_status', 'jpublish', 
					'image_tag', 'link_tag']
	list_filter = ('published_status', 'publish')
	search_fields = ('title', 'description')
	raw_id_fields = ('author',)
	list_editable = ('published_status',)
