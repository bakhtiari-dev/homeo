
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView

from .models import Article, Category
from site_setting.models import SiteSetting
from real_estate.models import Estate
from account.models import User


class ArticleList(TemplateView):
	"""
	Retrieve list of published articles, paginate them and send to the 
	template. This view also handle the search and filters objects by given 
	search key.
	"""
	def get(self, request, category_id=None, author_id=None, *args, **kwargs):
		articles = Article.published.select_related('author')

		search = request.GET.get('s', None)
		if search:
			articles = articles.filter(
				Q(title__contains=search) | 
				Q(description__contains=search) | 
				Q(author__first_name__contains=search)
			).distinct()

		# Filter articles by requested category
		category = None
		if category_id:
			category = get_object_or_404(Category, id=category_id)
			articles = articles.filter(categories=category)

		# Filter articles by requested author
		author = None
		if author_id:
			author = get_object_or_404(User.active.all(), id=author_id)
			articles = articles.filter(author=author)

		paginator = Paginator(articles, 4)
		page = request.GET.get('page', None)
		try:
			articles = paginator.page(page)
		except PageNotAnInteger:
			# if page is not an integer deliver the first page
			articles = paginator.page(1)
		except EmptyPage:
			# if page is out of range deliver last page of results
			articles = paginator.page(paginator.num_pages)		

		categories = Category.objects.all()

		# Last 3 published estates
		latest_estates = Estate.published.all()[:3]

		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 

		return render(request, 'blog/article_list.html',
					{'articles': articles, 
					'category': category, 
					'author': author,
					'site_setting': site_setting,
					'latest_estates': latest_estates,
					'categories': categories})


class ArticleDetail(TemplateView):
	"""Retrieve an article by id and raise a 404 error if not found."""	
	def get(self, request, article_id, *args, **kwargs):
		article = get_object_or_404(
			Article.published.select_related('author')
			.prefetch_related('categories'), id=article_id
		)

		categories = Category.objects.all()

		# Last 3 published estates
		latest_estates = Estate.published.all()[:3]

		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 

		return render(request, 'blog/article_detail.html',
					{'article': article,
					'site_setting': site_setting,
					'latest_estates': latest_estates,
					'categories': categories})
