from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('create-user/', views.CreateUserAPIView.as_view(), name='create-user'),
    path('generate-token/', ObtainAuthToken.as_view(), name='token-obtain'),
    path('weather/', views.WeatherData.as_view(), name = 'weather-data'),
    path('favorite-cities/', views.FavoriteCityListCreateView.as_view(), name='favorite-city-list-create'),
    path('search-history/', views.SearchHistoryListCreateView.as_view(), name='search-history-list-create'),

]
