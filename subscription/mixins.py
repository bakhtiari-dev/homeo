from django.http.response import HttpResponseRedirect
from django.urls.base import reverse

from .models import Subscription


class ActiveSubscriptionRedirectMixin():
	"""Redirect agent if he has an active subscription."""
	def dispatch(self, request, *args, **kwargs):
		agent = request.user
		subscription = Subscription.objects.filter(
			active=True, agent=agent
		).last()
		if subscription and subscription.is_active():
			return HttpResponseRedirect(reverse('site_setting:home'))
		return super().dispatch(request, *args, **kwargs)


class NotActiveSubscriptionRedirectMixin():
	"""Redirect agent if he does not have an active subscription."""
	def dispatch(self, request, *args, **kwargs):
		agent = request.user
		subscription = Subscription.objects.filter(
			active=True, agent=agent
		).last()
		if not subscription or not subscription.is_active():
			return HttpResponseRedirect(reverse('site_setting:home'))
		return super().dispatch(request, *args, **kwargs)


class BuySubscriptionMixin():
	"""Redirect agent if he has an active subscription."""
	def dispatch(self, request, *args, **kwargs):
		agent = request.user
		subscription = Subscription.objects.filter(
			active=True, agent=agent
		).last()
		if subscription and subscription.is_active():
			return HttpResponseRedirect(
				reverse('subscription:active_subscription_alert')
			)
		return super().dispatch(request, *args, **kwargs)
