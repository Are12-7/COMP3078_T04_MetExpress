from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('villages/', views.getVillages),
    path('villages/<str:id>/', views.getVillage)
]
