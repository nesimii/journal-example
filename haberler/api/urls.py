from django.urls import path

from haberler.api import views

urlpatterns = [
    path('makaleler/', views.makale_list_create_api_view, name='ma'),
    path('makaleler/<int:pk>/', views.makale_detail_api_view, name='makale-detay'),
]
