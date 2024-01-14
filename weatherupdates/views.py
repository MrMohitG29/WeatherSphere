from datetime import datetime
from rest_framework import status
import json
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import FavoriteCity, SearchHistory
from .serializers import UserSerializer, FavoriteCitySerializer, SearchHistorySerializer
from .config import OPENWEATHER_API_KEY, OPENWEATHER_API_URL


class CreateUserAPIView(APIView):
    """
    API view to create a new user.

    Methods:
    - post: Create a new user.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Create a new user.

        Parameters:
        - request: The HTTP request.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: JSON response.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeatherData(APIView):
    """
    API view to get weather data.

    Methods:
    - get: Get weather data based on the provided city name.
    """
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        Get weather data based on the provided city name.

        Parameters:
        - request: The HTTP request.

        Returns:
        - Response: JSON response with weather data.
        """
        name = request.query_params.get('name', 'Delhi')
        is_favorite_city = False

        api_key = OPENWEATHER_API_KEY
        url = OPENWEATHER_API_URL
        geocoding_url = f'{url}geo/1.0/direct?q={name}&limit=1&appid={api_key}'

        response = requests.get(geocoding_url)
        if response.status_code == 200:
            geocode_data = response.json()
            lat = geocode_data[0]['lat']
            lon = geocode_data[0]['lon']
            five_days_forecast_url = f'{url}data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}'

            response = requests.get(five_days_forecast_url)
            data = response.json()
            if request.user.is_authenticated:
                is_favorite_city = len(FavoriteCity.objects.filter(name=name, user = request.user)) > 0
                search_data = {'user': request.user.id, 'search_term': name.capitalize(), 'timestamp': datetime.now()}
                serializer = SearchHistorySerializer(data=search_data)
                if serializer.is_valid():
                    serializer.save()

            return Response({'data': data, 'isFavoriteCity': is_favorite_city})
        else:
            print('Error:', response.status_code, response.text)
            return Response({'cod': response.status_code, 'isFavoriteCity': False})

class FavoriteCityListCreateView(APIView):
    """
    API view to get or create favorite cities.

    Methods:
    - get: Get favorite cities for the authenticated user.
    - post: Create a new favorite city for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteCitySerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        """
        Get favorite cities for the authenticated user.

        Parameters:
        - request: The HTTP request.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - JsonResponse: JSON response with favorite cities.
        """
        favorite_cities = FavoriteCity.objects.filter(user=request.user)
        serializer = FavoriteCitySerializer(favorite_cities, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        """
        Create a new favorite city for the authenticated user.

        Parameters:
        - request: The HTTP request.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - JsonResponse: JSON response with the created favorite city.
        """
        name = request.query_params.get('name', '')
        if len(name) == 0:
            return JsonResponse(serializer.errors, status = 400)
        
        data = {'user': request.user.id, 'name': name.capitalize()}
        serializer = FavoriteCitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class SearchHistoryListCreateView(APIView):
    """
    API view to get or create search history.

    Methods:
    - get: Get search history for the authenticated user.
    - post: Create a new search history for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SearchHistorySerializer
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        """
        Get search history for the authenticated user.

        Parameters:
        - request: The HTTP request.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - JsonResponse: JSON response with search history.
        """
        search_history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
        serializer = SearchHistorySerializer(search_history, many=True)
        return JsonResponse(serializer.data, safe=False)
