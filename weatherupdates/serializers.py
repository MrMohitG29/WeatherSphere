# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FavoriteCity, SearchHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}



class FavoriteCitySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FavoriteCity
        fields = ['id', 'name', 'user']

class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SearchHistory
        fields = ['id', 'search_term', 'timestamp', 'user']
