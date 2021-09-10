from django.shortcuts import render
from django.views.generic import TemplateView

from .models import SiteSetting, Faq
from account.models import User
from blog.models import Article
from real_estate.models import Estate, City


class Home(TemplateView):
	"""Retrieve some objects to show in home page."""
	def get(self, request, *args, **kwargs):
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0]
		
		# Last 7 published estates
		estates = Estate.published.select_related('agent')[:7]

		# Last 7 active agents
		agents = User.active.all()[:7]

		# Last 3 published articles
		latest_articles = Article.published.select_related('author')[:3]

		# Get maximum amount of price, size and room to render search form in 
		# template.
		obj = Estate.published.all()
		if obj:
			max_price = obj.order_by('-price')[0].price
			max_size = obj.order_by('-size')[0].size
			max_room = obj.order_by('-room')[0].room
		else:
			max_price = 1000000
			max_size = 1000
			max_room = 10
			
		cities = City.objects.all()

		return render(request, 'site_setting/home.html',
					{'site_setting': site_setting, 
					'estates': estates, 
					'agents': agents,
					'latest_articles': latest_articles,
					'max_price':max_price, 
					'max_size': max_size, 
					'max_room': max_room,
					'cities': cities})
	

class AboutUs(TemplateView):
	def get(self, request, *args, **kwargs):
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0]
		
		# Count of active users, published articles and estates
		agents_count = User.active.count()
		estates_count = Estate.published.count()
		article_count = Article.published.count()

		return render(request, 'site_setting/about_us.html', 
					{'site_setting': site_setting, 
					'agents_count': agents_count, 
					'estates_count': estates_count,
					'article_count': article_count})


class FaqView(TemplateView):
	"""Retrieve list of faqs."""
	def get(self, request, *args, **kwargs):
		faqs = Faq.objects.all()
		
		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 
				
		return render(request, 'faq/faq.html', 
					{'faqs': faqs, 'site_setting': site_setting})


def not_found(request, exception):
	site_setting = SiteSetting.objects.filter(is_active=True)
	if site_setting:
		site_setting = site_setting[0]

	return render(request, '404.html', 
				  {'site_setting': site_setting})
