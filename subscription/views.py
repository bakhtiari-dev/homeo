from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Plan, Subscription
from .mixins import (
	ActiveSubscriptionRedirectMixin, NotActiveSubscriptionRedirectMixin, 
	BuySubscriptionMixin
)
from site_setting.models import SiteSetting


class PlanList(LoginRequiredMixin, TemplateView):
	"""Retrieve list of plans."""
	def get(self, request, *args, **kwargs):
		plans = Plan.objects.all()

		# Some settings of site such as footer context and ...
		site_setting = SiteSetting.objects.filter(is_active=True)
		if site_setting:
			site_setting = site_setting[0] 		
		return render(request, 'subscription/plans.html',
			{'plans': plans, 'site_setting': site_setting},
		)


class BuySubscription(LoginRequiredMixin, BuySubscriptionMixin, TemplateView):
	"""Get the plan and create a subscription for agent."""
	def get(self, request, plan_id, *args, **kwargs):
		plan = get_object_or_404(Plan, id=plan_id)
		agent = self.request.user
		from datetime import datetime, timedelta
		Subscription.objects.create(
			agent=agent,
			name=plan.name,
			price=plan.price,
			day_count=plan.day_count,
			estate_count=plan.estate_count,
			expiration_date=datetime.now() + timedelta(days=plan.day_count)
		)
		return redirect('account:subscription_list')


class SubscriptionAlert(LoginRequiredMixin, ActiveSubscriptionRedirectMixin, 
						TemplateView):
	def get(self, request, *args, **kwargs):
		return render(request, 'subscription/subscription_alert.html')


class ActiveSubscriptionAlert(LoginRequiredMixin, 
							  NotActiveSubscriptionRedirectMixin, 
							  TemplateView):
	def get(self, request, *args, **kwargs):
		return render(request, 'subscription/active_subscription_alert.html')
