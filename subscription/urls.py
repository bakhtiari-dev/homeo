from django.urls import path

from .views import (
	PlanList, SubscriptionAlert, BuySubscription, ActiveSubscriptionAlert
)


app_name = 'subscription'

urlpatterns = [
	path('plan/', PlanList.as_view(), name='plan_list'),
	path('subscription_alert/', SubscriptionAlert.as_view(), 
		 name='subscription_alert'),
	path('buy/<int:plan_id>/', BuySubscription.as_view(), 
		 name='buy_subscription'),
	path('active_subscription_alert/', ActiveSubscriptionAlert.as_view(), 
		 name='active_subscription_alert'),
]
