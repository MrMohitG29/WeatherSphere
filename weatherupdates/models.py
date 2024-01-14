from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class FavoriteCity(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.user.username}"
    

class SearchHistory(models.Model):
    search_term = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.search_term} - {self.timestamp}"