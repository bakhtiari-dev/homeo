from django.urls import path

from .views import ContactUs


app_name = 'contact_us'
urlpatterns = [
    path('', ContactUs.as_view(), name='contact_us')
]
