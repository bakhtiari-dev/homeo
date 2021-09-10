from django.urls import path

from .views import EstateList, EstateDetail


app_name = 'real_estate'

urlpatterns = [
    path('', EstateList.as_view(), name='estate_list'),
    path('<int:estate_id>/', EstateDetail.as_view(), name='estate_detail'),
    path('city/<int:city_id>/', EstateList.as_view(), 
         name='estate_list_by_city'),
    path('agent/<int:agent_id>/', EstateList.as_view(), 
         name='agent_estate_list'),
]
