from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import TemplateView

from .models import Estate, City
from site_setting.models import SiteSetting
from account.models import User


class EstateList(TemplateView):
	"""
	Retrieve list of published estates, paginate them and send to the template.
	This view also handle the search and filters objects by given search keys.
	"""
	def get(self, request, agent_id=None, city_id=None, *args, **kwargs):
		estates = Estate.published.select_related('agent', 'city')

		search = request.GET.get('search', None)
		if search:
			keys = request.GET
			estates = estates.filter(
				year__gte=keys['year_from'], year__lte=keys['year_to'], 
				size__gte=keys['size_from'], size__lte=keys['size_to'],
				price__gte=keys['price_from'], price__lte=keys['price_to'],
				room__gte=keys['room_from'], room__lte=keys['room_to']
			)
			if keys['text']:
				estates = estates.filter(
					Q(title__contains=keys['text']) | 
					Q(description__contains=keys['text'])
				)
			if keys['status']:
				estates = estates.filter(status=keys['status'])
			if keys['city']:
				estates = estates.filter(city=keys['city'])
			if keys['elevator']:
				estates = estates.filter(elevator=True)
			if keys['parking']:
				estates = estates.filter(parking=True)
			if keys['warehouse']:
				estates = estates.filter(warehouse=True)

		# Filter estates by requested agent
		agent = None
		if agent_id:
			agent = get_object_or_404(User.active.all(), id=agent_id)
			estates = estates.filter(agent=agent)

		# Filter estates by requested city
		city = None
		if city_id:
			city = get_object_or_404(City.objects.all(), id=city_id)
			estates = estates.filter(city=city)	

		paginator = Paginator(estates, 6)
		page = request.GET.get('page', None)
		try:
			estates = paginator.page(page)
		except PageNotAnInteger:
			# if page is not an integer deliver the first page
			estates = paginator.page(1)
		except EmptyPage:
			# if page is out of range deliver last page of results
			estates = paginator.page(paginator.num_pages)	

		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 

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

		return render(request, 'real_estate/estate_list.html',
					{'estates': estates, 
					'site_setting': site_setting,
					'agent': agent,
					'search': search,
					'max_price':max_price, 
					'max_size': max_size, 
					'max_room': max_room,
					'cities': cities})


class EstateDetail(TemplateView):
	"""Retrieve an estate by id and raise a 404 error if not found."""	
	def get(self, request, estate_id, *args, **kwargs):
		estate = get_object_or_404(
			Estate.published.select_related('agent', 'city')
							.prefetch_related('images'), 
							id=estate_id
		)

		# Last 3 published estates except current estate.
		latest_estates = Estate.published.all().exclude(id=estate.id)[:3]

		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 

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

		return render(request, 'real_estate/estate_detail.html',
					{'estate': estate, 
					'latest_estates': latest_estates,
					'site_setting': site_setting,
					'max_price': max_price, 
					'max_size': max_size, 
					'max_room': max_room,
					'cities': cities})
