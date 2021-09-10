from django.urls import path

from .views import Home, AboutUs, FaqView


app_name = 'site_setting'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about-us/', AboutUs.as_view(), name='about_us'),
    path('faq/', FaqView.as_view(), name='faq'),
]
