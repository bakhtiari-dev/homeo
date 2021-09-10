from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404

from real_estate.models import Estate
from blog.models import Article
from subscription.models import Subscription


class ArticleFieldsMixin():
	def dispatch(self, request, *args, **kwargs):
		self.fields = ["title", "description", 'image', "categories", 
					   "published_status"]
		return super().dispatch(request, *args, **kwargs)


class ArticleFormValidMixin():
	"""
	Set the current user as author of article and check the published status.
	"""
	def form_valid(self, form):
		self.obj = form.save(commit=False)
		self.obj.author = self.request.user
		if not self.obj.published_status in ['d', 'c']:
			self.obj.published_status = 'd'
		return super().form_valid(form)


class ArticleUpdateMixin():
	"""
	Raise a 404 error if user is not the author of article. It also raise if
	article's published status is checking.
	"""	
	def dispatch(self, request, pk, *args, **kwargs):
		article = get_object_or_404(Article, pk = pk)
		if article.published_status == 'c' or article.author != request.user:
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class ArticleDeleteMixin():
	"""
	A mixin that get the article and check who is asking for delete it.
	The app will raise a 404 error if user is not the author of article.
	"""
	def dispatch(self, request, pk, *args, **kwargs):
		article = get_object_or_404(Article, pk = pk)
		if article.author != request.user:
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class CheckSubscriptionMixin():
	"""Check the agent subscription."""
	def dispatch(self, request, *args, **kwargs):
		agent = request.user
		if agent.is_superuser:
			return super().dispatch(request, *args, **kwargs)

		subscription = Subscription.objects.filter(
			active=True, agent=agent
		).last()
		if not subscription or not subscription.is_active():
			return HttpResponseRedirect(
				reverse('subscription:subscription_alert')
			)
		return super().dispatch(request, *args, **kwargs)


class EstateFieldsMixin():
	def dispatch(self, request, *args, **kwargs):
		self.fields = [
			'city', 'title', 'description', 'status', 'size', 'price', 
			'monthly_rent', 'room', 'year', 'floor', 'elevator', 'parking', 
			'warehouse', 'published_status', 'main_image'
			]
		return super().dispatch(request, *args, **kwargs)


class EstateFormValidMixin():
	"""
	Set the current user as agent of estate and check the published status.
	Get the images from request and save them.
	"""	
	def form_valid(self, form):
		self.obj = form.save(commit=False)
		self.obj.agent = self.request.user
		if not self.obj.published_status in ['d', 'c']:
			self.obj.published_status = 'd'
		form.save()

		images = self.request.FILES.getlist('images')
		from real_estate.models import EstateImage
		for image in images:
			EstateImage.objects.create(estate=self.obj, image=image)
		return super().form_valid(form)


class AddCreatedEstatesMixin():
	"""
	Add one to the created estates after create a new estate.
	"""
	def form_valid(self, form):
		subscription = Subscription.objects.filter(
					active=True, agent=self.obj.agent
		).last()
		if subscription:
			subscription.created_estates += 1
			subscription.save()
		return super().form_valid(form)

class EstateUpdateMixin():
	"""
	Raise a 404 error if user is not the agent of estate. It also raise if
	estate's published status is checking.
	"""		
	def dispatch(self, request, pk, *args, **kwargs):
		estate = get_object_or_404(Estate, pk = pk)
		if estate.published_status == 'c' or estate.agent != request.user:
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class EstateDeleteMixin():
	"""
	A mixin that get the estate and check who is asking for delete it.
	The app will raise a 404 error if user is not the owner of estate.
	"""	
	def dispatch(self, request, pk, *args, **kwargs):
		estate = get_object_or_404(Estate, pk = pk)
		if estate.agent != request.user:
			raise Http404
		return super().dispatch(request, *args, **kwargs)


class LogInMixin():
	"""Redirect user to home page if he already logged in."""
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('site_setting:home'))
		return super().dispatch(request, *args, **kwargs)


class UserFieldsMixin():
	def dispatch(self, request, *args, **kwargs):
		self.fields = [
			'first_name', 'email', 'phone', 'description', 'image', 
			'website', 'facebook', 'twitter', 'linkedin', 'instagram', 
			'telegram', 'youtube'
			]
		return super().dispatch(request, *args, **kwargs)


class EmailVerifyRedirectMixin():
	"""Redirect user to estate list page if his email is already verified."""
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_email_verified:
			return HttpResponseRedirect(reverse('account:estate_list'))
		return super().dispatch(request, *args, **kwargs)


class CheckEmailActivationMixin():
	"""Redirect user to email_alert page if his email is not verified."""
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_email_verified:
			return HttpResponseRedirect(reverse('account:email_alert'))
		return super().dispatch(request, *args, **kwargs)
