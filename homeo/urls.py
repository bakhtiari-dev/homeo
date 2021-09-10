from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('agent/', include('account.urls')),
    path('estate/', include('real_estate.urls')),
    path('blog/', include('blog.urls')),
    path('contact-us/', include('contact_us.urls')),
    path('subscription/', include('subscription.urls')),

    path('', include('site_setting.urls')),
]

handler404 = 'site_setting.views.not_found'
