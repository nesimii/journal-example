from django.urls import path

from haberler.api import views

urlpatterns = [
    path('makaleler/', views.MakaleListAPIView.as_view(), name='ma'),
    path('makaleler/<int:pk>/', views.MakaleDetailAPIView.as_view(), name='makale-detay'),
]
